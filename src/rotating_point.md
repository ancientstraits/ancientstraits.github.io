Today, I figured out how to rotate a point to any angle.
It is actually much easier than it sounds to do.
I couldn't get a grasp of how to do it, but I tried this new strategy, and it might help you too.
The strategy revolves around the formulas used to rotate a point 90, 180, or 270 degrees.
This is very simple math that is learned in middle school.

# 90-degree increments
Take the point `(1, 2)` for example.
Rotation occurs counterclockwise, so rotating 90 degrees would give `(-2, 1)`,
rotating 180 degrees would give `(-1, -2)`, and rotating 270 degrees would give `(2, -1)`:
![image](https://github.com/ancientstraits/ancientstraits.github.io/assets/73802848/733a6f44-e944-4810-a867-fe10862a186b)

If we substitute `1` for `x` and `2` for `y`, we get:
```
Angle (degrees) | Point
--------------------------
0               | (x, y)
90              | (-y, x)
180             | (-x, -y)
270             | (y, -x)
```
Now, isolate the X-coordinate: `x, -y, -x, y`
And now, what happens if we write each x-coord as `ax + by`?
```
1x + 0y
0x + -1y
-1x + 0y
0x + 1y
```
Look at the X-coefficients: `1, 0, -1, 0`. Does that look familiar? Exactly.

# Trigonometry time
```
Angle (degrees) | cos(angle) | sin(angle)
-----------------------------------------
0               |  1         |  0
90              |  0         |  1
180             | -1         |  0
270             |  0         | -1
```
The X-coefficients are the same as `cos`,
while the Y-coefficients are like `sin`, but with opposite signs, so `-sin`.
Thus, the rotated X-coordinate is `cos(angle)*x - sin(angle)*y`.

# Y coordinate
We can use the same method for the Y-coordinates:
```
0x + 1y
1x + 0y
0x + -1y
-1x + 0y
```
The X-coefficients are `sin`, and the Y-coefficients are `cos`,
so we get `sin(angle)*x + cos(angle)*y`.

This means that when rotating `(x, y)` by angle `a`,
`newX = xcos(angle) - ysin(a)`, and `newY = xsin(a) + ycos(a)`.
In other words, the rotated point is `(xcos(a) - ysin(a), xsin(a) + ycos(a))`.

# Matrices
I was learning how to rotate a point for OpenGL, and graphics programmers like to use matrices to rotate points.
You could very easily do this with matrices
```
I lost interest here because matrices are very boring to explain, but you could multiply a vector by a rotation matrix.
It does the same thing as the newX and newY thing does.
```
