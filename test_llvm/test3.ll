@.str = private unnamed_addr constant [3 x i8] c"%d ", align 1 
define i32 @main() #0 { 
%a = alloca i32 
%.r1 = load i32 , i32* %a
%.r2 = alloca i32
store i32 321 , i32* %.r2
%.r3 = alloca i32
store i32 123 , i32* %.r3
%.r4 = mul i32 %.r2 , %.r3 
store i32 %.r4 , i32* %a
%.r5 = alloca i32
store i32 23 , i32* %.r5
ret i32 %.r5 
} 
declare i32 @printf(i8*, ...) #1