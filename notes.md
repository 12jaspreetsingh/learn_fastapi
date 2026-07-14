from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello"}
    
    Here, @app.get("/") is a decorator. It tells FastAPI: "When an HTTP GET request comes to /, execute the home() function."
    
    A decorator is essentially a function that takes another function, adds some behavior, and returns a new function. It lets you extend functionality cleanly and reuse common logic across many functions without modifying their original implementations.
    
    
    import asyncio

async def main():
    print("Start")
    await asyncio.sleep(5)
    print("End")

asyncio.run(main())
Looks similar.

But there is one huge difference.

Instead of blocking,

await asyncio.sleep(5)

means

"I'm waiting.
If there is other work, go do that."

The CPU is free.
What is Blocking?

Imagine downloading a file.

Download...

takes 10 seconds.

Sync:

Download file

(wait)

Continue

Nothing else happens.

Async:

Start download

Go do something else

When download finishes,
continue.
def hello():
    print("Hi")
Runs immediately.
async def hello():
    print("Hi")
Calling it doesn't execute it immediately.

hello()

returns a coroutine object.

To actually run it, you must await it from another async function or use asyncio.run().

await hello()

or
asyncio.run(hello())
When should you use async in FastAPI?

Use async def when your endpoint spends time waiting on operations such as:

Database queries using an async database driver
HTTP requests to other APIs
Reading or writing files asynchronously
Any async library that you can await

Use a normal def when the endpoint mainly performs CPU-intensive work, such as:

Large numerical computations
Image processing
Machine learning inference (unless using an async API around it)






