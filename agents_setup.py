from agents import Agent,Runner,RunContextWrapper,input_guardrail,TResponseInputItem,GuardrailFunctionOutput,InputGuardrailTripwireTriggered,trace
from config import rununer_config
from pydantic import BaseModel
from typing import Any

# Data Classes

class QuizType(BaseModel):
    question:str
    option_1:str
    option_2:str
    option_3:str
    option_4:str
    correct_answer:str

class QuizList(BaseModel):
    quiz:list[QuizType]

class QuizSetup(BaseModel):
    limit:int
    difficulty:str

class isQuizPrompt(BaseModel):
    isQuizPrompt:bool


async def the_quiz_room(Qlimit:int,Qdifficulty:str,Qinput:str) -> str|list :

    # Context
    quiz_setup = QuizSetup(
        limit=Qlimit,
        difficulty=Qdifficulty
    )

    # Instruction Function

    def quiz_instructions(ctx:RunContextWrapper[QuizSetup],agent:Agent) -> str:
        return f"You are a **quiz agent**, Your task is to generate **{ctx.context.limit}** quizez based on user query, Quiz difficulty level will be **{ctx.context.difficulty}**"



    # Guardrails

    quiz_validator = Agent(
        name="Quiz Generation Validator",
        instructions="You are a Quiz Generation Validator. Your task is to analyze the user's request and determine if it is suitable for generating a quiz.",
        output_type=isQuizPrompt
    )

    @input_guardrail
    async def quiz_input_guardrail(ctx:RunContextWrapper[None], agent:Agent[Any], input:str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
        result = await Runner.run(quiz_validator,input,run_config=rununer_config,context=ctx.context)
        return GuardrailFunctionOutput(
            output_info="None",
            tripwire_triggered= not result.final_output.isQuizPrompt
        )

    # Agennts and Runner Setup

    quiz_agent = Agent(
        name="Quiz Agent",
        instructions=quiz_instructions,
        output_type=QuizList,
        input_guardrails=[quiz_input_guardrail]
    )
    
    try:
        with trace("The Quiz Room(Agent)"):
            result = await Runner.run(
                starting_agent=quiz_agent,
                input = Qinput,
                run_config=rununer_config,
                context=quiz_setup
            )
            return result.final_output
        
    except InputGuardrailTripwireTriggered:
        return "Please Enter Prompt related to quiz topic or enter your syllabus, we can't generate prompt from your query, please try agin with different query."
    except:
        return "Something went wrong, Please Try again"

