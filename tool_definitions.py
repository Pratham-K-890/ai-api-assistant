


calculator_tool = {
   "type":"function",
   "function":{
      "name":"calculator",
      "description":"This function should be called whenever an arithmetic operation is needs to be performed",
      "parameters":{
         "type":"object",
         "properties":{
            "a":{
               "type":"number",
               "description":"This is an operand"
            },
            "operation":{
               "type":"string",
               "description":"The arithmetic operation. Must be exactly one of: 'add', 'subtract', 'multiply', 'divide'"
            },
            "b":{
               "type":"number",
               "description":"This is an operand"
            }
         },
         "required":["a","b","operation"]
      }
   }
}    

weather_tool={
   "type":"function",
   "function":{
      "name":"weather",
   "description":"ALWAYS use this tool to get weather information for any city. Never answer weather questions from your own knowledge. Always call this tool when the user asks about weather.",
   "parameters":{
      "type":"object",
      "properties":{
         "city":{
            "type":"string",
            "description":"this a name of a city which is a datatype of string"
         }
      },
      "required":["city"]
      }
   }
   
}

search_tool={
    "type":"function",
    "function":{
        "name":"search",
        "description":"Use this tool to search for current events, recent news, or information that may have changed after 2024. Do NOT use for general knowledge questions like definitions, concepts, or well-known facts",
        "parameters":{
            "type":"object",
            "properties":{
                "query":{
                    "type":"string",
                    "description":"The thing you need to search you can make yourself a query for the things you need to know and pass that as a parameter"
                }
            },
            "required":["query"]
        }
    }
}