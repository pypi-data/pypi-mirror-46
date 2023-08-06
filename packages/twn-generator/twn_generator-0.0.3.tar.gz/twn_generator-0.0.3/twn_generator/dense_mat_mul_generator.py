#! /usr/bin/python3

import csv

def make_ROM( weights, no_vecs, bw_w, rom_name = "w_mem" ):
    assert len(weights) % no_vecs == 0, "len(weights) must be divisible by no_vecs"
    fmt = "00" + str( bw_w ) + "b"
    no_cycs = int( len(weights) / no_vecs )
    no_bits_each_cyc = no_vecs*bw_w * len( weights[0] )
    rom_txt = "reg [" + str( no_cycs - 1 ) + ":0][" + str( len(weights[0]) - 1 ) + ":0][" + str( no_vecs*bw_w - 1) + ":0]" + rom_name + ";\n"
    rom_txt += "initial begin\n"
    for i in range( no_cycs ):
        rom_txt += rom_name + "[" + str(i) + "] = "
        rom_txt += str( no_bits_each_cyc ) + "'b"
        subset = np.transpose( weights[i*no_vecs:(i+1)*no_vecs] )
        for j in range( len( subset ) ):
            rom_txt += "".join( [ format( v + ( 1 << bw_w ), fmt )[-bw_w:] for v in subset[j] ] )
        rom_txt += ";\n"
    rom_txt += "end\n"
    return rom_txt

def DMM_generate( fname_w, module_name, BW_in, BW_out, cycles ):
    f = open( fname_w )
    rdr = csv.reader( f )
    weights = np.array( [ [ int(x) for x in y ] for y in rdr ] )
    f.close()
    max_val = np.max( weights )
    if max_val > 0:
        max_val += 1  # eg) log2(2) => 1 but needs 2 bits
    bits_max = np.ceil( np.log2( np.abs( max_val ) ))
    min_val = np.min( weights )
    if min_val != 0:
        bits_min = np.ceil( np.log2( np.abs( min_val ) ))
    else:
        bits_min = 0
    # determine the bitwidth needed for the weights
    bits_w = max( bits_max, bits_min )
    if min_val < 0: # add a bit for sign
        bits_w += 1
    no_inputs = len(weights)
    no_outputs = len( weights[0] )
    no_vecs = int( no_inputs/cycles )
    log2_cyc = int( np.ceil( np.log2( cycles ) ) )
    log2_no_vecs = int( np.ceil( np.log2( no_vecs ) ) )
    module_header = "module " + module_name + """ (
input clock,
input reset,
input vld_in,
input [""" + str( no_vecs - 1) + ":0][" + str(BW_in-1) + """:0] in,
output vld_out,
output [""" + str( no_outputs - 1) + ":0][" + str(BW_out-1) + """:0] out
);
"""
    module_body = make_ROM( weights, no_vecs, bits_w, "w_mem" )
    if cycles > 1:
        module_body += "reg [" + str( log2_cyc - 1 ) + """:0] cntr;
always @( posedge clock ) begin
  if ( reset ) begin
    cntr <= 0;
  end else begin
    if ( vld_in ) begin
      if ( cntr >= """ + str( cycles - 1 ) + """) begin
         cntr <= 0;
      end else begin
         cntr <= cntr + 1;
      end
    end
  end
end
"""
    else: # if all in one cycle
        module_body += "wire cntr;\nassign cntr = 0;\n"
    # w_mem[cntr][i] gets the weights for this cycle and filter i
    module_body += """
genvar i;
generate
multiply_accumulate
  #(
    .LOG2_NO_VECS(""" + str(log2_no_vecs) + """),
    .BW_IN(""" + str( BW_in ) + """),
    .BW_OUT(""" + str( BW_out ) + """),
    .BW_W(""" + str( bits_w ) + """)
) (
  .clk(clock),
  .new_sum(cntr == 0),
  .data_in(in),
  .w_vec( w_mem[cntr] ),
  .data_out( out[i] )
);
endgenerate
    """
    # make the ROM with the weights values
    module_body += "endmodule\n"
    return module_header + module_body
