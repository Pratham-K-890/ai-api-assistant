from ddgs import DDGS



def calculate(a,b,operation):
    if operation=="add":
      return a+b
    elif operation=="subtract":
       return a-b
    elif operation=="multiply":
       return a*b
    elif operation=="divide":
       if b==0: return "Error: division by zero"
       return a/b    
    else: return "Error: unknown operation"

def get_weather(city):
    return f"The weather in {city} is 28°C and sunny."

def search(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))

    output=""
    for r in results:
        output+=f"Title:{r['title']}\n"
        output+=f"Body:{r['body']}\n\n"

    return output