import("stdfaust.lib");
declare options "[osc:on]";

process(freq, gain) = os.osc(freq) * gain : ve.moog_vcf(0.1, freq);