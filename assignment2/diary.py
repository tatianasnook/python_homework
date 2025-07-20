import traceback

# Task 1.
try:
    with open("diary.txt", "a") as file:
        prompt = 'What happened today? (Type "done for now" to finish) '
        while True:
            answer = input(prompt)
            file.write(answer + "\n")
            if answer == "done for now":
                break
            prompt = 'What else? (Type "done for now" to finish) '

except Exception as e:
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append(
            f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")
    print(f"Stack trace: {stack_trace}")
