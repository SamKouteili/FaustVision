import("stdfaust.lib");

right = !, _;
left = _, !;

dec(x) = x - int(x);

// generates sawtooth signal \in [0,1] at freq f
phase(f) = f/ma.SR : (+:dec) ~ _;
sawtooth(phase) = phase * 2 - 1;


process(freq, amp) = phase(freq) : sawtooth * amp;


