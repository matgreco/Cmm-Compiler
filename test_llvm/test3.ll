 @.str = private unnamed_addr constant [3 x i8] c"%d ", align 1 
define i32 @main() #0 { 
%a = alloca i32 
%.r1 = load i32 , i32* %a
%.r2 = add i32 321 , 0
%.r3 = add i32 123 , 0
%.r4 = mul i32 %.r2 , %.r3 
store i32 %.r4 , i32* %a
%.r5 = load i32 , i32* %a
%.r6 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), i32 %.r5) 
%.r7 = add i32 23 , 0
ret i32 %.r7 
} 
declare i32 @printf(i8*, ...) #1