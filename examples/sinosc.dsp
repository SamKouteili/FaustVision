import("stdfaust.lib");
declare options "[osc:on]";

process(freq, gain) = os.oscsin(freq) * gain;
