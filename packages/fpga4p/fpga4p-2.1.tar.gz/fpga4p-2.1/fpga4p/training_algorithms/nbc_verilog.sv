module BC_UART
#(
    parameter AMOUNT_CLASS                          = x,
    parameter WIDTH_FIFO_RX                         = x,
    parameter string  INIT_MEM_CAL[AMOUNT_CLASS-1:0]= '{ },
   
    parameter WIDTH_LOG_W                           = 32,
    parameter WIDTH_LOG_D                           = 32,
    parameter WIDTH_LOG_V                           = 32,
    parameter ORDER_UART                            = 1
)
(
    input  logic rst,
    input  logic clk_10MGz,
    input  logic clk,

    input  logic rx,
    output logic rts,
    output logic tx

//    input  logic cts

);
logic cts;
assign cts = 0;

// fifoRX
logic                            we_fifoRX;
logic [WIDTH_FIFO_RX-1:0]        wdata_fifoRX;
logic                            full_fifoRX;

// fifoTX
logic                            re_fifoTX;
logic [7:0]                      rdata_fifoTX;
logic                            empty_fifoTX;

//logic clk_10MGz;
logic clk_2;

/*
PLL PLL_1
    (
        .inclk0                 (clk),
        .c0                     (clk_10MGz),
        .c1                     (clk_2)
    );
*/

interface_UART
    #(
        .WIDTH_FIFO_RX          (WIDTH_FIFO_RX),
        .ORDER                  (ORDER_UART)
    )
interface_UART_1
    (
        .rst                    (rst),
        .clk_10MHz              (clk_10MGz),

        .rx                     (rx),
        .rts                    (rts),
        .tx                     (tx),
        .cts                    (cts),

        .empty                  (empty_fifoTX),
        .rdata                  (rdata_fifoTX),
        .re                     (re_fifoTX),

        .full                   (full_fifoRX),
        .wdata                  (wdata_fifoRX),
        .we                     (we_fifoRX)
    );


Bayes_class
    #(
        .AMOUNT_CLASS           (AMOUNT_CLASS),
        .WIDTH_FIFO_RX          (WIDTH_FIFO_RX),
        .INIT_MEM_CAL           (INIT_MEM_CAL),
        .WIDTH_LOG_W            (WIDTH_LOG_W),
        .WIDTH_LOG_D            (WIDTH_LOG_D),
        .WIDTH_LOG_V            (WIDTH_LOG_V)
    )
Bayes_class_1
    (
        .rst                    (rst),
        .clk_1                  (clk_10MGz),
        .clk_2                  (clk),

        .we_fifoRX              (we_fifoRX),
        .wdata_fifoRX           (wdata_fifoRX),
        .full_fifoRX            (full_fifoRX),

        .re_fifoTX              (re_fifoTX),
        .rdata_fifoTX           (rdata_fifoTX),
        .empty_fifoTX           (empty_fifoTX)
    );




endmodule

//===================================================================
//===================================================================
//===================================================================

module fifo
#(
    parameter WIDTH_DATA = 32,
    parameter MEM_SIZE   = 16 // 2**MEM_SIZE слов будет в памяти
)
(
    input logic rst,
    input logic clk_we,
    input logic clk_re,

    input logic                     we,
    input logic [WIDTH_DATA-1:0]    wdata,
    output logic full,

    input logic                     re,
    output logic [WIDTH_DATA-1:0]   rdata,
    output logic                    empty
);
logic we_mem;
logic re_mem;

logic [MEM_SIZE:0] we_point;
logic [MEM_SIZE:0] re_point;
logic [MEM_SIZE:0] we_point_grey;
logic [MEM_SIZE:0] re_point_grey;
logic [MEM_SIZE:0] we_point_grey_tout;
logic [MEM_SIZE:0] re_point_grey_tout;
logic [MEM_SIZE:0] we_point_grey_t1;
logic [MEM_SIZE:0] re_point_grey_t1;
logic [MEM_SIZE:0] we_point_grey_t2;
logic [MEM_SIZE:0] re_point_grey_t2;
logic [MEM_SIZE:0] we_point_decodeGrey;
logic [MEM_SIZE:0] re_point_decodeGrey;

logic [MEM_SIZE:0] we_point_grey_plus_one;
logic [MEM_SIZE:0] re_point_grey_plus_one;


mem_fifo #(WIDTH_DATA,MEM_SIZE) ram_with_2clk
    (
        .rst            (rst),
        .clk_we         (clk_we),
        .clk_re         (clk_re),

        .we             (we_mem),
        .we_point       (we_point[MEM_SIZE-1:0]),
        .wdata          (wdata),

        .re             (re_mem),
        .re_point       (re_point[MEM_SIZE-1:0]),
        .rdata          (rdata)
    );

assign we_mem = (~full) ? we : 0;
assign re_mem = (~empty) ? re : 0;

always_ff @(negedge rst,posedge clk_we)
    if(~rst) we_point<=0;
    else if(we && ~full) we_point <=we_point+1;

always_ff @(negedge rst,posedge clk_re)
    if(~rst) re_point <=0;
    else if(re && ~empty) re_point <=re_point+1;

assign we_point_grey = we_point ^ (we_point>>1);
assign we_point_grey_plus_one = (we_point+(we && ~full)) ^ ((we_point+(we && ~full))>>1);
assign re_point_grey = re_point ^ (re_point>>1);
assign re_point_grey_plus_one = (re_point+(re && ~empty)) ^ ((re_point+(re && ~empty))>>1);

always_ff @(negedge rst,posedge clk_we)
    if(~rst) we_point_grey_tout <=0;
    else we_point_grey_tout <= we_point_grey;

always_ff @(negedge rst,posedge clk_re)
    if(~rst) re_point_grey_tout <=0;
    else re_point_grey_tout <= re_point_grey;

always_ff @(negedge rst,posedge clk_re)
    if(~rst) begin
        we_point_grey_t1 <=0;
        we_point_grey_t2 <=0;
    end
    else begin
        we_point_grey_t1 <= we_point_grey_tout;
        we_point_grey_t2 <= we_point_grey_t1;
    end

always_ff @(negedge rst,posedge clk_we)
    if(~rst) begin
        re_point_grey_t1 <=0;
        re_point_grey_t2 <=0;
    end
    else begin
        re_point_grey_t1 <=re_point_grey_tout;
        re_point_grey_t2 <=re_point_grey_t1;
    end

always_ff @(negedge rst,posedge clk_we)
    if(~rst) full <=0;
    else if((we_point_grey_plus_one[MEM_SIZE] != re_point_grey_t2[MEM_SIZE]) &&
            (we_point_grey_plus_one[MEM_SIZE-1] != re_point_grey_t2[MEM_SIZE-1]) &&
            (we_point_grey_plus_one[MEM_SIZE-2:0] == re_point_grey_t2[MEM_SIZE-2:0]))
            full <=1;
    else full <=0;

always_ff @(negedge rst,posedge clk_re)
    if(~rst) empty <=1;
    else if(re_point_grey_plus_one == we_point_grey_t2)
        empty <=1;
    else empty <=0;

endmodule


//===================================================================
//===================================================================
//===================================================================

module controller
#(
    parameter AMOUNT_CLASS        = 4,
    parameter WIDTH_FIFO_RX       = 8,
    parameter WIDTH_LOG_W         = 16,
    parameter WIDTH_LOG_D         = 16,
    parameter WIDTH_LOG_V         = 16,
    parameter WIDTH_LOG_N         = 16 // пока будет равно WIDTH_FIFO_RX
)
(
    input logic rst,
    input logic clk,

    // rx_fifo
    input  logic                      empty,
    output logic                      re,
    input  logic [WIDTH_FIFO_RX-1:0]  data_in,
    // tx_fifo
    input  logic                      full,
    output logic                      we,
    output logic  [7:0]               data_out,

    output logic                     enable,
    output logic  [WIDTH_LOG_N-1:0]  amount_word,
    output logic  [WIDTH_LOG_D-1:0]  log_D [AMOUNT_CLASS-1:0],
    output logic  [WIDTH_LOG_V-1:0]  log_V [AMOUNT_CLASS-1:0],

    input  logic [$clog2(AMOUNT_CLASS):0]   class_win,
    output logic                            finish
);
localparam bitINclass_win = $clog2(AMOUNT_CLASS) + 1;
localparam bytesINword =
                (bitINclass_win % 8 == 0) ?
                    bitINclass_win / 8 : (bitINclass_win / 8) + 1;

logic [1:0] count_param; //кол-во параметров, если что поправить разрядность.
logic re_t1;

logic [$clog2(bytesINword)+1:0] counter_we;
logic [7:0] data_buf[bytesINword-1:0];
logic [bytesINword*8-1:0] expansion_class_win;



initial begin
    $readmemh("data_log_D.dat",log_D);
    $readmemh("data_log_V.dat",log_V);
end

always_ff @(negedge rst,posedge clk)
    if(~rst)
        re_t1 <= 0;
    else
        re_t1 <= re;

typedef enum logic [2:0] {  wait_start_S,
                            read_param_S,
                            inprogress_S,
                            write_data_S,
                            end_S       ,
                            ping_S      } statetype;
statetype state,nextstate;

always_ff @(negedge rst,posedge clk)
    if(~rst)
        state <= wait_start_S;

    else
        state <= nextstate;

always_comb
    case(state)
        wait_start_S:
                        if(&data_in)
                            nextstate = read_param_S;

                        else if( &data_in[WIDTH_FIFO_RX-1:2]  &&
                                 ~data_in[1]                  &&
                                  data_in[0]                  &&
                                  re_t1                       )

                            nextstate = ping_S;

                        else
                            nextstate = wait_start_S;
        read_param_S:
                        if(count_param == 1)
                            nextstate = inprogress_S;
                        else
                            nextstate = read_param_S;
        inprogress_S:
                        if(re_t1 && &data_in[WIDTH_FIFO_RX-1:1] && ~data_in[0])
                            nextstate = write_data_S;
                        else
                            nextstate = inprogress_S;
        write_data_S:
                        if(we && counter_we == bytesINword + 2 - 1)
                            nextstate = end_S;
                        else
                            nextstate = write_data_S;
        end_S        :
                        if(&data_in)
                            nextstate = read_param_S;

                        else if( &data_in[WIDTH_FIFO_RX-1:2]  &&
                                 ~data_in[1]                  &&
                                  data_in[0]                  &&
                                  re_t1                       )

                            nextstate = ping_S;

                        else
                            nextstate = end_S;
        ping_S      :
                        if(~full)
                            nextstate = wait_start_S;
                        else
                            nextstate = ping_S;
        default        :
                        nextstate = wait_start_S;
    endcase

always_ff @(negedge rst,posedge clk)
    if(~rst)
        count_param <= 0;

    else if(state == read_param_S && re)
        count_param <= count_param + 1;

    else
        count_param <= 0;

always_ff @(negedge rst,posedge clk)
    if(~rst)
        amount_word <= 0;

    else if(state == read_param_S && count_param == 1)
        amount_word <= data_in;


always_comb
    case(state)
        inprogress_S:
                        if(re_t1 && ~(&data_in[WIDTH_FIFO_RX-1:1] && ~data_in[0]))
                            enable = 1;
                        else
                            enable = 0;
        default       :
                        enable = 0;
    endcase

always_comb
    case(state)
        wait_start_S:
                        if( &data_in[WIDTH_FIFO_RX-1:2]  &&
                            ~data_in[1]                  &&
                             data_in[0]                  &&
                             re_t1                       )

                            re = 0;

                        else if(~empty && ~(&data_in))
                            re = 1;
                        else
                            re = 0;
        read_param_S:
                        if(~empty && count_param < 1)
                            re = 1;
                        else
                            re = 0;
        inprogress_S:
                        if(~empty && ~(&data_in[WIDTH_FIFO_RX-1:1] && ~data_in[0]))
                            re = 1;
                        else
                            re = 0;
        end_S       :
                        if( &data_in[WIDTH_FIFO_RX-1:2]  &&
                            ~data_in[1]                  &&
                             data_in[0]                  &&
                             re_t1                       )

                            re = 0;

                        else if(~empty && ~(&data_in))
                            re = 1;
                        else
                            re = 0;
        default     :
                        re = 0;
    endcase

assign finish = (state == end_S) ? 1 : 0;


//=====================================================
//                    begin: downsizer
//=====================================================



always_ff @(negedge rst,posedge clk)
    if(~rst)
        counter_we <= 0;

    else if(state == write_data_S && we && counter_we == bytesINword + 2 - 1)
        counter_we <= 0;

    else if(state == write_data_S && we)
        counter_we <= counter_we + 1;


always_comb
    if(state == ping_S && ~full)
        we = 1;

    else if(state == write_data_S && ~full)
        we = 1;

    else
        we = 0;

generate

    if(bitINclass_win % 8 == 0)
        assign expansion_class_win = class_win;
    else
        assign expansion_class_win[bitINclass_win-1:0] = class_win;
        assign expansion_class_win[bytesINword*8-1:bitINclass_win] = 0;

    genvar i;
    for(i = 0; i < bytesINword; i++) begin : create_data_buf
        always_ff @(negedge rst,posedge clk)
            if(~rst)
                data_buf[i] <= 0;

            else if(state == inprogress_S       &&
                    re_t1                       &&
                    &data_in[WIDTH_FIFO_RX-1:1] &&
                    ~data_in[0])

                data_buf[i] <= expansion_class_win[bytesINword*8 - 1 - i*8 :
                                                   bytesINword*8 - 8 - i*8];
    end

endgenerate


always_comb
    if(state == ping_S)
        data_out = 8'b01010111;

    else if(counter_we == 0)
        data_out = ~0;

    else if(counter_we == bytesINword + 2 - 1)begin
        data_out[0] = 1'b0;
        data_out[7:1] = ~0;
    end
    else if(counter_we > 0)
        data_out = data_buf[counter_we - 1];
    else
        data_out = 0;
//=====================================================
//                    end: downsizer
//=====================================================

endmodule

//================================================================
//================================================================
//================================================================


module calculator
#(
    parameter AMOUNT_CLASS      = 4,
    parameter INIT_MEM_FILE     = " ",
    parameter NUMBER            = 0,
    parameter WIDTH_FIFO_RX     = 8,
    parameter WIDTH_LOG_W       = 16,
    parameter WIDTH_LOG_D       = 16,
    parameter WIDTH_LOG_V       = 16,
    parameter WIDTH_LOG_N       = 16 // пока будет равно WIDTH_FIFO_RX
)
(
    input logic rst,
    input logic clk,

    //из контроллера
    input logic                             finish,
    input logic                             enable,
    input logic [WIDTH_LOG_N-1:0]           amount_word,
    input logic [WIDTH_LOG_D-1:0]           log_D,
    input logic [WIDTH_LOG_V-1:0]           log_V,

    //из fifo
    input logic [WIDTH_FIFO_RX-1:0]         data_in,

    output logic [127:0]                    data_out, // сколько битов нужно ?
    output logic [$clog2(AMOUNT_CLASS):0]   number
);
localparam WIDTH_NMULLOGV = (WIDTH_LOG_N > WIDTH_LOG_V) ? 2*WIDTH_LOG_N : 2*WIDTH_LOG_V;

logic finish_t1;
logic finish_fall;

logic re_memRO;
logic re_memRO_t1;
logic [WIDTH_FIFO_RX-1:0] addr_memRO;
logic [WIDTH_LOG_W-1:0] data_memRO;

logic [WIDTH_NMULLOGV-1:0] nMULlogV;
logic [127:0] sum_log_W;  //  сколько битов нужно ?

assign number = NUMBER;

always_ff @(negedge rst,posedge clk)
    if(~rst)
        finish_t1 <= 0;
    else
        finish_t1 <= finish;

assign finish_fall = (~finish && finish_t1) ? 1 : 0;

memRO
    #(
        .INIT_MEM_FILE      (INIT_MEM_FILE),
        .WIDTH_DATA         (WIDTH_LOG_W),
        .WIDTH_ADDR         (WIDTH_FIFO_RX)
    )
ramRO
    (
        .clk                (clk),

        .re                 (re_memRO),
        .addr               (addr_memRO),
        .data               (data_memRO)
    );

assign addr_memRO = data_in;
assign re_memRO = enable;

always_ff @(negedge rst,posedge clk)
    if(~rst)
        re_memRO_t1 <= 0;

    else
        re_memRO_t1 <= re_memRO;

always_ff @(negedge rst,posedge clk)
    if(~rst)
        sum_log_W <= 0;

    else if(re_memRO_t1)
        sum_log_W <= sum_log_W + data_memRO;

    else if(finish_fall)
        sum_log_W <= 0;

assign nMULlogV = log_V * amount_word;
assign data_out = nMULlogV - log_D - sum_log_W;

endmodule


//==================================================================
//==================================================================
//==================================================================


module Bayes_class
#(
    parameter AMOUNT_CLASS                          = 4,
    parameter WIDTH_FIFO_RX                         = 8,
    parameter string INIT_MEM_CAL[AMOUNT_CLASS]     = {
                                                        "../test/data_log_W_0.dat",
                                                        "../test/data_log_W_1.dat"
                                                        },
    parameter WIDTH_LOG_W                           = 16,
    parameter WIDTH_LOG_D                           = 16,
    parameter WIDTH_LOG_V                           = 16
)
(
    input  logic rst,
    input  logic clk_1,
    input  logic clk_2,

    // fifoRX
    input  logic                            we_fifoRX,
    input  logic [WIDTH_FIFO_RX-1:0]        wdata_fifoRX,
    output logic                            full_fifoRX,

    // fifoTX
    input  logic                            re_fifoTX,
    output logic [7:0]                      rdata_fifoTX,
    output logic                            empty_fifoTX

);
localparam WIDTH_LOG_N = WIDTH_FIFO_RX;//in future, maybe change
localparam MEMSIZE_FIFO_RX = 8;

logic re_fifoRX;
logic [WIDTH_FIFO_RX-1:0] rdata_fifoRX;
logic empty_fifoRX;

logic we_fifoTX;
logic full_fifoTX;
logic [7:0] wdata_fifoTX;

logic  enable;
logic  [WIDTH_LOG_N-1:0] amount_word;
logic  [WIDTH_LOG_D-1:0] log_D [AMOUNT_CLASS-1:0];
logic  [WIDTH_LOG_V-1:0] log_V [AMOUNT_CLASS-1:0];
logic  [$clog2(AMOUNT_CLASS):0] number [AMOUNT_CLASS-1:0];

logic [127:0] calcul_out[AMOUNT_CLASS-1:0]; // how many bits are needed ?

logic [$clog2(AMOUNT_CLASS):0]   class_win;
logic finish;

fifo
    #(
        .WIDTH_DATA                 (WIDTH_FIFO_RX),
        .MEM_SIZE                   (MEMSIZE_FIFO_RX)
    )
fifoRX_bayes
    (
        .rst                        (rst),
        .clk_we                     (clk_1),
        .clk_re                     (clk_2),

        .we                         (we_fifoRX),
        .wdata                      (wdata_fifoRX),
        .full                       (full_fifoRX),

        .re                         (re_fifoRX),
        .rdata                      (rdata_fifoRX),
        .empty                      (empty_fifoRX)
    );

fifo
    #(
        .WIDTH_DATA                 (8),// note: convention is that ->
        .MEM_SIZE                   (4)//  -> TX fifo`s width equally 8 bit
    )
fifoTX_bayes
    (
        .rst                        (rst),
        .clk_we                     (clk_2),
        .clk_re                     (clk_1),

        .we                         (we_fifoTX),
        .wdata                      (wdata_fifoTX),
        .full                       (full_fifoTX),

        .re                         (re_fifoTX),
        .rdata                      (rdata_fifoTX),
        .empty                      (empty_fifoTX)
    );

controller
    #(
        .AMOUNT_CLASS               (AMOUNT_CLASS),
        .WIDTH_FIFO_RX              (WIDTH_FIFO_RX),
        .WIDTH_LOG_D                (WIDTH_LOG_D),
        .WIDTH_LOG_V                (WIDTH_LOG_V),
        .WIDTH_LOG_N                (WIDTH_LOG_N)
    )
controller_bayes
    (
        .rst                        (rst),
        .clk                        (clk_2),

        .empty                      (empty_fifoRX),
        .re                         (re_fifoRX),
        .data_in                    (rdata_fifoRX),

        .full                       (full_fifoTX),
        .we                         (we_fifoTX),
        .data_out                   (wdata_fifoTX),

        .enable                     (enable),
        .amount_word                (amount_word),
        .log_D                      (log_D),
        .log_V                      (log_V),

        .class_win                  (class_win),
        .finish                     (finish)
    );


generate
genvar i;


    for(i = 0; i < AMOUNT_CLASS; i++)begin:create_calcul

        calculator
            #(
                .AMOUNT_CLASS               (AMOUNT_CLASS),
                .INIT_MEM_FILE              (INIT_MEM_CAL[i]),
                .NUMBER                     (i),//core number
                .WIDTH_FIFO_RX              (WIDTH_FIFO_RX),
                .WIDTH_LOG_W                (WIDTH_LOG_W),
                .WIDTH_LOG_D                (WIDTH_LOG_D),
                .WIDTH_LOG_V                (WIDTH_LOG_V),
                .WIDTH_LOG_N                (WIDTH_LOG_N)
            )
        calculator_bayes
            (
                .rst                        (rst),
                .clk                        (clk_2),

                .finish                     (finish),
                .enable                     (enable),
                .amount_word                (amount_word),
                .log_D                      (log_D[i]),
                .log_V                      (log_V[i]),

                .data_in                    (rdata_fifoRX),

                .data_out                   (calcul_out[i]),
                .number                     (number[i])
            );
    end


endgenerate

tree_comparator
    #(
        .WIDTH_DATA         (128),
        .AMOUNT_CLASS       (AMOUNT_CLASS)
    )
tree_comparator_bayes
    (
        .data               (calcul_out),
        .number             (number),

        .class_win          (class_win)
    );

endmodule


//================================================================
//================================================================
//================================================================

module tree_comparator
#(
    parameter WIDTH_DATA       = 8,
    parameter AMOUNT_CLASS     = 5
)
(
    input logic [WIDTH_DATA-1:0]            data[AMOUNT_CLASS-1:0],
    input logic [$clog2(AMOUNT_CLASS):0]    number [AMOUNT_CLASS-1:0],

    output logic [$clog2(AMOUNT_CLASS):0]   class_win
);

comparator
        #(
            .AMOUNT_CLASS               (AMOUNT_CLASS),
            .WIDTH_DATA                 (WIDTH_DATA),
            .LVL_TREE                   (AMOUNT_CLASS)// самый высокий
        )                                              // уровень равен AMOUNT_CLASS

comparator_root
        (
            .data                       (data),
            .number                     (number),

            .more                       (),
            .class_win                  (class_win)
        );



endmodule

module comparator
#(
    parameter AMOUNT_CLASS      = 8,
    parameter WIDTH_DATA        = 8,
    parameter LVL_TREE          = 5// постпено убывает
)
(
    input logic [WIDTH_DATA-1:0]            data[LVL_TREE-1:0],
    input logic [$clog2(AMOUNT_CLASS):0]    number[LVL_TREE-1:0],

    output logic [WIDTH_DATA-1:0]           more,
    output logic [$clog2(AMOUNT_CLASS):0]   class_win
);
localparam LVL_NEXT_LEFT = LVL_TREE / 2;
localparam LVL_NEXT_RIGHT = ((LVL_TREE % 2) == 0) ? (LVL_TREE / 2) :
                                                            ((LVL_TREE / 2) + 1);

generate
    if(LVL_TREE == 1)begin

        assign more = data[0];
        assign class_win = number[0][$clog2(AMOUNT_CLASS):0];

    end

    else if(LVL_TREE == 2) begin

        assign more = (data[0] < data[1]) ? data[0] : data[1];

        assign class_win = (data[0] < data[1]) ? number[0] : number[1];

    end

    else if(LVL_TREE >= 3)begin

        logic [WIDTH_DATA - 1:0] more_left, more_right;
        logic [$clog2(AMOUNT_CLASS):0] class_win_left, class_win_right;

        logic [WIDTH_DATA - 1:0] data_left[LVL_NEXT_LEFT - 1:0];
        logic [WIDTH_DATA - 1:0] data_right[LVL_NEXT_RIGHT - 1:0];

        logic [$clog2(AMOUNT_CLASS):0] number_left[LVL_NEXT_LEFT - 1:0];
        logic [$clog2(AMOUNT_CLASS):0] number_right[LVL_NEXT_RIGHT - 1:0];

        assign number_left[LVL_NEXT_LEFT - 1:0] = number[LVL_NEXT_LEFT - 1:0];
        assign number_right[LVL_NEXT_RIGHT - 1:0] = number[LVL_TREE - 1:LVL_NEXT_LEFT];
        
        assign data_left[LVL_NEXT_LEFT - 1:0] = data[LVL_NEXT_LEFT - 1:0];
        assign data_right[LVL_NEXT_RIGHT - 1:0] = data[LVL_TREE - 1:LVL_NEXT_LEFT];

        assign more = (more_left < more_right) ? more_left : more_right;

         assign class_win = (more_left < more_right) ? class_win_left : class_win_right;

        comparator
            #(
                .AMOUNT_CLASS               (AMOUNT_CLASS),
                .WIDTH_DATA                 (WIDTH_DATA),
                .LVL_TREE                   (LVL_NEXT_LEFT)
            )
        comparator_left
            (
                .data                       (data_left),
                .number                     (number_left),

                .more                       (more_left),
                .class_win                  (class_win_left)
            );

        comparator
            #(
                .AMOUNT_CLASS               (AMOUNT_CLASS),
                .WIDTH_DATA                 (WIDTH_DATA),
                .LVL_TREE                   (LVL_NEXT_RIGHT)
            )
        comparator_right
            (
                .data                       (data_right),
                .number                     (number_right),

                .more                       (more_right),
                .class_win                  (class_win_right)
            );
    end
endgenerate



endmodule

//=================================================================
//=================================================================
//=================================================================
module mem_fifo
#(
    parameter WD = 32,
    parameter mem_size = 16
)
(
    input logic rst,
    input logic clk_we,
    input logic clk_re,

    input logic we,
    input logic [mem_size-1:0] we_point,
    input logic [WD-1:0] wdata,
    
    input logic re,
    input logic [mem_size-1:0] re_point,
    output logic [WD-1:0] rdata
);
logic [WD-1:0] ram[2**mem_size-1:0];


always_ff @(negedge rst,posedge clk_we)
    if(~rst) 
        for(int i=0; i<2**mem_size;i++)begin
            ram[i]<=0;
        end
    else if(we) ram[we_point][WD-1:0] <=wdata[WD-1:0];

always_ff @(negedge rst,posedge clk_re)
    if(~rst) rdata <=0;
    else if(re) rdata <=ram[re_point];

endmodule 
//=================================================================
//=================================================================
//=================================================================

module interface_UART
#(
    parameter WIDTH_FIFO_RX     = 8,
    parameter ORDER             = 0 // 1 - first received bit is low, 0  - high 
)
(
    input logic  rst,
    input logic  clk_10MHz,
    
    input  logic rx,
    output logic rts,
    output logic tx,
    input  logic cts, 
    
    input  logic empty,
    input  logic [7:0] rdata,
    output logic re,
    
    input  logic full,
    output logic [WIDTH_FIFO_RX-1:0] wdata,
    output logic we
     
);
localparam clk_divider = 520;// it is need for 9600 bod rate

logic uart_order;
logic rx_t1,rx_t2,rx_t3;
logic cts_t1,cts_t2,cts_t3;
logic tx_inside;
logic [31:0] counter_clk_rx;
logic [31:0] counter_clk_tx;
logic clk_rx_div;
logic clk_tx_div;
logic clk_rx;
logic clk_tx;
logic [5:0] counter_bit_rx;
logic [5:0] counter_bit_tx;
logic empty_t1;
logic empty_fall;
logic cts_fall; 
logic we2upsizer;
logic [7:0] data2upsizer;
logic uart_tx_inprogress;
logic uart_rx_inprogress;
assign uart_order = ORDER;

assign rts = full;

//================== tt ==============
always_ff @(negedge rst,posedge  clk_10MHz)
    if(~rst) begin 
        rx_t1 <= 1;
        rx_t2 <= 1;
        rx_t3 <= 1;
    end
    else begin 
        rx_t1 <= rx;
        rx_t2 <= rx_t1;
        rx_t3 <= rx_t2;        
    end


//==================== rx busy ===========
always_ff @(negedge rst,posedge clk_10MHz)
    if(~rst) 
        uart_rx_inprogress <=0;
        
    else if(clk_rx && counter_bit_rx==10)
        uart_rx_inprogress <=0;
    
    else if(~rx_t2 && rx_t3) 
        uart_rx_inprogress <=1;

//==================== clk_divider_rx ===========
always_ff @(negedge rst,posedge clk_10MHz)
    if(~rst) begin 
        counter_clk_rx <= 0;
        clk_rx_div <= 0;
    end
    else if(~uart_rx_inprogress)begin 
        counter_clk_rx <= 0;
        clk_rx_div <= 0;
    end
    else if(counter_clk_rx == clk_divider - 1) begin 
        counter_clk_rx <= 0;
        clk_rx_div <= ~clk_rx_div;
    end
    else  counter_clk_rx <= counter_clk_rx + 1;

assign clk_rx = (~clk_rx_div && counter_clk_rx==clk_divider-1) ? 1 : 0;
//=================== counter_bit_rx ============
always_ff @(negedge rst,posedge clk_10MHz)
    if(~rst)
        counter_bit_rx <= 0;

    else if(clk_rx && counter_bit_rx == 10)
        counter_bit_rx <= 0;

    else if(clk_rx)
        counter_bit_rx <= counter_bit_rx + 1;


//================= data_rx ================
always_ff @(negedge rst,posedge clk_10MHz)
    if(~rst)
        data2upsizer <= 0; 

    else if(clk_rx && uart_order) 
        data2upsizer <= {rx_t3,data2upsizer[7:1]};
    
    else if(clk_rx && ~uart_order) 
        data2upsizer <= {data2upsizer[6:0],rx_t3};


always_ff @(negedge rst,posedge clk_10MHz)
    if(~rst) 
        we2upsizer <= 0;
        
    else if(we2upsizer) 
        we2upsizer <= 0;
        
    else if(clk_rx && counter_bit_rx == 8) 
        we2upsizer <= 1;


//=====================================================
//                    begin: upsizer
//=====================================================        
generate begin: upsizer
localparam bytesINword = ((WIDTH_FIFO_RX % 8) == 0) ? 
                                  WIDTH_FIFO_RX / 8 : (WIDTH_FIFO_RX / 8) + 1;
                                
localparam remainder   = WIDTH_FIFO_RX % 8;


    
    if(WIDTH_FIFO_RX <= 8)begin 
 
        assign we = we2upsizer;       
        
        if(remainder == 0) 
            assign wdata = data2upsizer;
        
        else 
            assign wdata = data2upsizer[remainder-1:0]; 
        
    end
    else begin
        logic [0:bytesINword-2][7:0] part_wdata; // less than wdata (one byte)  
        logic [$clog2(bytesINword)+1:0]  counter_byte;

        always_ff @(negedge rst,posedge clk_10MHz)
            if(~rst) 
                counter_byte <= 0;
        
            else if(we2upsizer && counter_byte == bytesINword - 1)
                counter_byte <= 0;
            
            else if(we2upsizer)
                counter_byte <= counter_byte + 1;

    
        always_ff @(negedge rst,posedge clk_10MHz)
            if(~rst)
                part_wdata <= 0;
            
            else if(we2upsizer)
                part_wdata[counter_byte] <= data2upsizer;

        if(remainder == 0)
            assign wdata = {part_wdata, data2upsizer};
        
        else if(bytesINword == 2)
            assign wdata = {part_wdata[0][remainder-1:0], data2upsizer};      
        
        else           
            assign wdata = {part_wdata[0][remainder-1:0], 
                            part_wdata[1:bytesINword-2], data2upsizer};

                   
        assign we = (we2upsizer && counter_byte == bytesINword-1) ? 1 : 0;   

    end          

end                  
endgenerate 
//=====================================================
//                    end: upsizer
//=====================================================    

        
//================= empty && cts ===============
always_ff @(negedge rst,posedge clk_10MHz)
    if(~rst) 
        empty_t1 <= 1;
    else     
        empty_t1 <= empty;

always_ff @(negedge rst,posedge clk_10MHz)
    if(~rst) begin
        cts_t1 <= 1;
        cts_t2 <= 1;
        cts_t3 <= 1;
    end
    else begin
        cts_t1 <= cts;
        cts_t2 <= cts_t1;
        cts_t3 <= cts_t2; 
    end

assign empty_fall = (~empty  && empty_t1) ? 1 : 0;
assign cts_fall   = (~cts_t2 &&   cts_t3) ? 1 : 0;
 
//================ clk_divider_tx ==========
always_ff @(negedge rst,posedge  clk_10MHz)
    if(~rst)
        uart_tx_inprogress <= 0;
        
    else if(clk_tx && ~cts_t2 && ~empty && counter_bit_tx == 9)
        uart_tx_inprogress <= 1;
        
    else if(clk_tx && (cts_t2 || empty) && counter_bit_tx == 9)
        uart_tx_inprogress <= 0;
     
    else if((empty_fall || cts_fall) && ~uart_tx_inprogress && ~empty && ~cts_t2)
        uart_tx_inprogress <= 1;
        
        
always_ff @(negedge rst,posedge clk_10MHz)
    if(~rst) begin 
        counter_clk_tx <= 0;
        clk_tx_div <= 0;
    end
    else if(~uart_tx_inprogress)begin 
        counter_clk_tx <= 0;
        clk_tx_div <= 0;
    end
    else if(counter_clk_tx == clk_divider-1) begin 
        counter_clk_tx <= 0;
        clk_tx_div <= ~clk_tx_div;
    end
    else  counter_clk_tx <= counter_clk_tx +1;

assign clk_tx = (~clk_tx_div && counter_clk_tx==clk_divider-1) ? 1:0;
//=============== counter_bit_tx ==============
always_ff @(negedge rst,posedge  clk_10MHz)
    if(~rst) 
        counter_bit_tx <= 0;

    else if(clk_tx && counter_bit_tx==10)
        counter_bit_tx <= 0;

    else if(clk_tx)begin 
        counter_bit_tx <= counter_bit_tx + 1;
    end


always_ff @(negedge rst,posedge  clk_10MHz)
    if(~rst)
        re <= 0;
        
    else if(re)
        re <= 0;
    
    else if(clk_tx && ~cts_t2 && ~empty && counter_bit_tx == 9)
        re <= 1;
     
    else if((empty_fall || cts_fall) && ~uart_tx_inprogress && ~empty && ~cts_t2)
        re <= 1;
        
//=============== tx =============
always_comb
    case(counter_bit_tx)
        0:  tx_inside = 1;
        1:  tx_inside = 0;
        10: tx_inside = 1;
        default: begin 
                    if(uart_order)  
                        tx_inside = rdata[counter_bit_tx - 2];
                    else 
                        tx_inside = rdata[8 - 1 - counter_bit_tx + 2];
                 end
    endcase
    
always_ff @(negedge rst,posedge  clk_10MHz)
    if(~rst)
        tx <= 1;
    else
        tx <= tx_inside;

endmodule 

//=================================================================
//=================================================================
//=================================================================
module memRO
#(
    parameter INIT_MEM_FILE     = " ",
    parameter WIDTH_DATA        = 32,
    parameter WIDTH_ADDR        = 16 // 2**mem_size слов в памяти
)
(
    input logic clk,

    input logic re,
    input logic [WIDTH_ADDR-1:0] addr,
    output logic [WIDTH_DATA-1:0] data

);
logic [WIDTH_DATA-1:0] ram[2**WIDTH_ADDR-1:0];

initial begin 
    $readmemh(INIT_MEM_FILE,ram);                                            
end


always_ff @(posedge clk)
    if(re) 
        data <= ram[addr];
    
    else 
        data <= 0;

endmodule 
//=================================================================
//=================================================================
//=================================================================
