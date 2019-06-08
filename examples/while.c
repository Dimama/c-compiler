int main()
{
	int i = 0;
	while(i < 10)
	{
		i = i + 1;
	}
	i = i * 2;
	printstr("i = ");
	print_int(i);
}

void print_int(int a){
	asm("li $v0 1");
	asm("syscall");
}