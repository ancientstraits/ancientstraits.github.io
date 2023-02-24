---
title: Neural Networks #0: Creating a One-Weight Program
---

# Introduction
I am trying to learn machine learning.
In order to do this, I will write a tiny neural network in C.

In this network, we will only have an input value, an output value, and a weight.
The input value will be known as `x`, and the weight will be known as `w`.
The output value will be equal to the input multiplied by the weight, so it is `w*x`.
The goal of the program is to make the output value of the neuron equal to the input.
In other words, `w*x=x`.
We know that `w` must be 1 in order for the output to equal the input.
However, the computer does not know this, and it is its goal to get as close to 1 as possible.

# The model and error checking
First, implement the `outval` function to compute the output value (`out=w*x`):
```c
float outval(float w, float x) {
	return w * x;
}
```

Then, implement the error.
It is common to use `(a-b)^2` as a measure of how far `a` is from `b`,
because as `b` get closer to `a`, the slope of the function gets closer to zero,
which is great for training (later in this post).
```c
float err(float a, float b) {
	return (a-b)*(a-b);
}
```

We just want the error as a function of the weight, for any value of `x`.
To do this, create a function that calculates the average error when `0 <= x < 1`:
```c
float avg_err(float w) {
	const float dx = 0.001;
	int num_subdiv = 0;
	float sum = 0.0;

	for (float x = 0.0; x < 1.0; x += dx, num_subdiv++) {
		// got: outval(w, x)
		// expected: x
		sum += err(outval(w, x), x);
	}

	return sum / (float)num_subdiv;
}
```

# Learning and Gradient Descent
Now that we have a way to calculate the error of `w`,
how do we adjust them to be better?
Our `avg_err` function has a minimum of 0.
We can calculate the (average) slope of this `avg_err` function.
Then, we subtract our slope from our weight to get closer to the minimum of the function.
For example, if there is a negative slope, then we add the opposite (a positive number)
to our weight, to get closer to the minimum.
Since `(a-b)^2` is a quadratic function, its minimum has a slope of zero.
As `w` gets closer to 1, the `avg_err` function's slope gets closer to zero.
We can use this to find the minimum of the error, or where the model functions best.

Write a function to calculate the slope of the error:
```c
float err_slope(float w) {
	const float dw = 0.0001;
	float err1 = avg_err(w), err2 = avg_err(w + dw);
	return (err2 - err1) / dw;
}
```
The closer `dw` is to 0, the more exact this slope is.
It just uses the formula `slope = (y1-y2)/(x1-x2)`.
In this case, it is `(avg_err(w+dw)-avg_err(w))/((w+dw)-(w))`,
or `(avg_err(w+dw)-avg_err(w))/dw`.

Now, we will write a function to subtract the slope from w.
the `learn_rate` is multiplied by the slope to make sure that `w`
does not "jump over" the minimum.
For me, however, `1.0` worked well enough.
The function is called `epoch` since each stage of training is an "epoch".
```c
// returns a new value of w.
float epoch(float w) {
	const float learn_rate = 1.0;

	float slope = err_slope(w);
	printf("slope = %f; ", slope);
	// found local minimum

	return w - (learn_rate * slope);
}
```

# Wrapping it Up
Finally, it is time to write the `main` function.
It will train the model, print out statistics, and test the model after 100 rounds.
```c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define ROUNDS 100

// ...

int main() {
	float w = 0.0;
	int weight_correct;

	for (int i = 0; i < ROUNDS; i++) {
		printf("Round %d: w is %f; ", i, w);
		w = epoch(w);
		printf("w becomes %f\n", w);

	}

	printf("Final model: outval(0.3) = %f\n", outval(w, 0.3));

	return 0;
}
```

After running and compiling the code, we get the output:
```
$ ./neuron
Round 0: w is 0.000000; slope = -0.668168; w becomes 0.668168
Round 1: w is 0.668168; slope = -0.221133; w becomes 0.889301
Round 2: w is 0.889301; slope = -0.073803; w becomes 0.963104
Round 3: w is 0.963104; slope = -0.024586; w becomes 0.987690
Round 4: w is 0.987690; slope = -0.008179; w becomes 0.995868
Round 5: w is 0.995868; slope = -0.002723; w becomes 0.998591
Round 6: w is 0.998591; slope = -0.000906; w becomes 0.999498
Round 7: w is 0.999498; slope = -0.000302; w becomes 0.999799
Round 8: w is 0.999799; slope = -0.000100; w becomes 0.999900
Round 9: w is 0.999900; slope = -0.000033; w becomes 0.999933
Round 10: w is 0.999933; slope = -0.000011; w becomes 0.999944
Round 11: w is 0.999944; slope = -0.000004; w becomes 0.999948
Round 12: w is 0.999948; slope = -0.000001; w becomes 0.999949
Round 13: w is 0.999949; slope = -0.000000; w becomes 0.999950
Round 14: w is 0.999950; slope = -0.000000; w becomes 0.999950

...

Round 94: w is 0.999950; slope = -0.000000; w becomes 0.999950
Round 95: w is 0.999950; slope = -0.000000; w becomes 0.999950
Round 96: w is 0.999950; slope = -0.000000; w becomes 0.999950
Round 97: w is 0.999950; slope = -0.000000; w becomes 0.999950
Round 98: w is 0.999950; slope = -0.000000; w becomes 0.999950
Round 99: w is 0.999950; slope = -0.000000; w becomes 0.999950
Final model: neuron(0.3) = 0.299985
```

Our model was able to get extremely close to `w = 1`. Very nice.
You can find the source code [here](https://gist.github.com/ancientstraits/936fecd67681fba309c76be57fe3b945).

# More Applications
What if the input value is added to, not multiplied by, the weight to get the output?
This means that `out=w+x`.
(In this case, `w` is not a weight, but a **bias**, since it is used for addition,
not multiplication.)

If we want the output to be equal to the input, or `w+x=x`, w has to be zero.
Can the program do this? Yes!

All we have to do is change the return statement of `outval`:
```
float outval(float w, float x) {
	return w + x;
}
```
We must also change `learn_rate` in `epoch()` to `0.1`,
or it will "jump over" the minimum.
In `main()`, `w` should be initialized to something other than `0.0`,
because we want to see the neural network train itself.

After compiling, and running, this is the result:
```
$ ./neuron
Round 0: w is 1.000000; slope = 1.949072; w becomes 0.805093
Round 1: w is 0.805093; slope = 1.597404; w becomes 0.645352
Round 2: w is 0.645352; slope = 1.287758; w becomes 0.516577
Round 3: w is 0.516577; slope = 1.051426; w becomes 0.411434
Round 4: w is 0.411434; slope = 0.789464; w becomes 0.332488
Round 5: w is 0.332488; slope = 0.648722; w becomes 0.267615
Round 6: w is 0.267615; slope = 0.538304; w becomes 0.213785
Round 7: w is 0.213785; slope = 0.422858; w becomes 0.171499
Round 8: w is 0.171499; slope = 0.343304; w becomes 0.137169
Round 9: w is 0.137169; slope = 0.274647; w becomes 0.109704
Round 10: w is 0.109704; slope = 0.219373; w becomes 0.087767

...

Round 95: w is -0.000050; slope = 0.000000; w becomes -0.000050
Round 96: w is -0.000050; slope = 0.000000; w becomes -0.000050
Round 97: w is -0.000050; slope = 0.000000; w becomes -0.000050
Round 98: w is -0.000050; slope = 0.000000; w becomes -0.000050
Round 99: w is -0.000050; slope = 0.000000; w becomes -0.000050
Final model: outval(0.3) = 0.299950
```

And the modified program has come very close as well to what we wanted (w=0)!
This scenario shows how neural networks can very easily adapt to different scenarios.

# Conclusion
(I hope that) this is the first (zeroth) blog post in a series on
how to make neural networks.
I do not really know a lot about neural networks,
so I hope I can build one without having to learn or teach
anything related to calculus or matrices or statistics.

Perhaps in the next blog post, I will make a neural network with more than one
input value, or input neuron.

