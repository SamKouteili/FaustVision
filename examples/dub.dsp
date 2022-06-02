import("stdfaust.lib");
declare options "[osc:on]";

process(freq, gain) = sy.dubDub(freq,100,2,1)*gain;