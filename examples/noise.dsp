import("stdfaust.lib");
declare options "[osc:on]";

process(freq, gain) = no.noise*gain;
