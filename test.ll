@.str = private unnamed_addr constant [3 x i8] c"%d ", align 1 
define i32 @main() #0 { 
%a = alloca i32 
%.r1 = load i32 , i32* %a
%.r2 = alloca i32
store i32 321 , i32* %.r2
store i32 %.r2 , i32* %a
%.r3 = load i32 , i32* %a
%.r4 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), i32 %.r3)%.r5 = alloca i32
store i32 999 , i32* %.r5
ret i32 0 
} 
declare i32 @printf(i8*, ...) #1