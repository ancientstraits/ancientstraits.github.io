# Introduction
My favorite way to read files as of writing this is via memory-mapped file IO.
Using this technique creates a buffer based on the file which can be read from like a string.
No `fread()`, `fgets()`, `fgetc()`, or any of that.
It also is not needed to `malloc()` a whole new memory buffer and copy the file contents to it.
However, there is not much information on how to do this online, especially when compared to other, perhaps inferior, techniques.
My favorite (and only) resource of recounting how this technique works is [Jacob Sorber's video](https://www.youtube.com/watch?v=m7E9piHcfr4), and I am writing this post so I can more quickly find out how to use memory-mapped files if I ever forget.

# The Code
```c
int main() {
	// First, open the file
	int fd = open("filename", O_RDONLY);
	// Then, get the length of the file
	struct stat sb;
	fstat(fd, &sb);
    // sb.st_size is the length
	// Finally, use `mmap()`
	char* file = mmap(NULL,
		sb.st_size, // the memory region should be as large as the file
		PROT_READ, // readonly memory
		MAP_PRIVATE, // can probably also be `MAP_SHARED`
		fd, // get the data from our file descriptor
		0 // start at the file's beginning
	);

	// `file` can be used like any other memory buffer
	// For example, the following code prints the file
	for (int i = 0; i < sb.st_size; i++)
		putchar(file[i]);

	// Finish everything
	munmap(file, sb.st_size);
	close(fd);
}
```

# Conclusion
`mmap()` is a great file IO method, since it is both easy to write and also speedy.
One problem is that `mmap()` is POSIX, meaning that it works on Linux, MacOS, and other Unix operating systems, but not Windows.
However, this caveat is a minor afterthought to me, since I have not used Windows for more than a year.

