"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: converse.py
Description: An extra cognitive module for generating conversations. 
"""
import math
import sys
import datetime
import random
sys.path.append('../')

from global_methods import *

from persona.memory_structures.spatial_memory import *
from persona.memory_structures.associative_memory import *
from persona.memory_structures.scratch import *
from persona.cognitive_modules.retrieve import *
from persona.prompt_template.run_gpt_prompt import *

def generate_agent_chat_summarize_ideas(init_persona, 
                                        target_persona, 
                                        retrieved, 
                                        curr_context): 
  all_embedding_keys = list()
  for key, val in retrieved.items(): 
    for i in val: 
      all_embedding_keys += [i.embedding_key]
  all_embedding_key_str =""
  for i in all_embedding_keys: 
    all_embedding_key_str += f"{i}\n"

  try: 
    summarized_idea = run_gpt_prompt_agent_chat_summarize_ideas(init_persona,
                        target_persona, all_embedding_key_str, 
                        curr_context)[0]
  except:
    summarized_idea = ""
  return summarized_idea


def generate_summarize_agent_relationship(init_persona, 
                                          target_persona, 
                                          retrieved): 
  all_embedding_keys = list()
  for key, val in retrieved.items(): 
    for i in val: 
      all_embedding_keys += [i.embedding_key]
  all_embedding_key_str =""
  for i in all_embedding_keys: 
    all_embedding_key_str += f"{i}\n"

  summarized_relationship = run_gpt_prompt_agent_chat_summarize_relationship(
                              init_persona, target_persona,
                              all_embedding_key_str)[0]
  return summarized_relationship


def generate_agent_chat(maze, 
                        init_persona, 
                        target_persona,
                        curr_context, 
                        init_summ_idea, 
                        target_summ_idea): 
  summarized_idea = run_gpt_prompt_agent_chat(maze, 
                                              init_persona, 
                                              target_persona,
                                              curr_context, 
                                              init_summ_idea, 
                                              target_summ_idea)[0]
  for i in summarized_idea: 
    print (i)
  return summarized_idea


def agent_chat_v1(maze, init_persona, target_persona): 
  # Chat version optimized for speed via batch generation
  curr_context = (f"{init_persona.scratch.name} " + 
              f"was {init_persona.scratch.act_description} " + 
              f"when {init_persona.scratch.name} " + 
              f"saw {target_persona.scratch.name} " + 
              f"in the middle of {target_persona.scratch.act_description}.\n")
  curr_context += (f"{init_persona.scratch.name} " +
              f"is thinking of initating a conversation with " +
              f"{target_persona.scratch.name}.")

  summarized_ideas = []
  part_pairs = [(init_persona, target_persona), 
                (target_persona, init_persona)]
  for p_1, p_2 in part_pairs: 
    focal_points = [f"{p_2.scratch.name}"]
    retrieved = new_retrieve(p_1, focal_points, 50)
    relationship = generate_summarize_agent_relationship(p_1, p_2, retrieved)
    focal_points = [f"{relationship}", 
                    f"{p_2.scratch.name} is {p_2.scratch.act_description}"]
    retrieved = new_retrieve(p_1, focal_points, 25)
    summarized_idea = generate_agent_chat_summarize_ideas(p_1, p_2, retrieved, curr_context)
    summarized_ideas += [summarized_idea]

  return generate_agent_chat(maze, init_persona, target_persona, 
                      curr_context, 
                      summarized_ideas[0], 
                      summarized_ideas[1])


#주석 처리
def generate_one_utterance(init_persona, target_persona, retrieved, curr_chat): 
#def generate_one_utterance( init_persona, target_persona, curr_chat): 
  # Chat version optimized for speed via batch generation

  print ("July 23 5")
  if(target_persona):
    curr_context = (f"{init_persona.scratch.act_description} " + 
              f"{init_persona.scratch.name}이(가) " + 
              f"{target_persona.scratch.name}을(를) 보았을 때 " + 
              f"{target_persona.scratch.act_description}.\n")
    curr_context += (f"{init_persona.scratch.name}은(는) " +
              f"{target_persona.scratch.name}와(과) 대화를 시작하고 있다. ")
  
    x = run_gpt_generate_iterative_chat_utt(init_persona, target_persona, retrieved, curr_context, curr_chat)[0]
    #x = run_gpt_generate_iterative_chat_utt(init_persona, target_persona, curr_context, curr_chat)[0]
  else:
    curr_context = (f"{init_persona.scratch.name} " + 
              f"was {init_persona.scratch.act_description} " + 
              f"when {init_persona.scratch.name} " + 
              f"saw User")
    curr_context += (f"{init_persona.scratch.name} " +
              f"is initiating a conversation with User")
    x = run_gpt_generate_iterative_user_chat_utt(init_persona, retrieved, curr_context, curr_chat)[0]

  print ("July 23 6")

  print ("adshfoa;khdf;fajslkfjald;sdfa HERE", x)

  return x["utterance"], x["end"]

def agent_chat_v2(init_persona, target_persona): 
  curr_chat = []
  print ("July 23")
  for i in range(1): 
    focal_points = [f"{target_persona.scratch.name}"]
    print("focal_points: ", focal_points)
    # 주석 처리
    retrieved = new_retrieve(init_persona, focal_points, 50)
    
    print('\n--------------- retrieved for convo ----------------: \n', retrieved)
    for key, val in retrieved.items():
      print("'", key, "': ")
      for i in val:
        print(i.type, " / ", i.spo_summary())
    print("----------------------------------------------------\n")
    
    relationship = generate_summarize_agent_relationship(init_persona, target_persona, retrieved)
    print ("-------- relationship", relationship)
    last_chat = ""
    for i in curr_chat[-4:]:
      last_chat += ": ".join(i) + "\n"
    if last_chat: 
      focal_points = [f"{relationship}", 
                      f"{target_persona.scratch.name} is {target_persona.scratch.act_description}", 
                      last_chat]
    else: 
      focal_points = [f"{relationship}", 
                      f"{target_persona.scratch.name} is {target_persona.scratch.act_description}"]
    print("new focal_points: ", focal_points)
    retrieved = new_retrieve(init_persona, focal_points, 15)
    
    print('\n------------------ new retrieved for convo --------------------: \n', retrieved)
    for key, val in retrieved.items():
      print("'", key, "': ")
      for i in val:
        print(i.type, " / ", i.spo_summary())
    print("---------------------------------------------------------------\n")
    
    utt, end = generate_one_utterance(init_persona, target_persona, retrieved, curr_chat)
    #utt, end = generate_one_utterance(init_persona, target_persona, curr_chat)

    curr_chat += [[init_persona.scratch.name, utt]]
    if end:
      break


    focal_points = [f"{init_persona.scratch.name}"]
    print("target focal_points: ", focal_points)
    retrieved = new_retrieve(target_persona, focal_points, 50)
    
    print('\n----------------- target retrieved for convo -------------------: \n', retrieved)
    for key, val in retrieved.items():
      print("'", key, "': ")
      for i in val:
        print(i.type, " / ", i.spo_summary())
    print("-----------------------------------------------------------------\n")
    
    relationship = generate_summarize_agent_relationship(target_persona, init_persona, retrieved)
    print ("-------- relationshopadsjfhkalsdjf", relationship)
    last_chat = ""
    for i in curr_chat[-4:]:
      last_chat += ": ".join(i) + "\n"
    if last_chat: 
      focal_points = [f"{relationship}", 
                      f"{init_persona.scratch.name} is {init_persona.scratch.act_description}", 
                      last_chat]
    else: 
      focal_points = [f"{relationship}", 
                      f"{init_persona.scratch.name} is {init_persona.scratch.act_description}"]
    print("target new focal_points: ", focal_points)
    retrieved = new_retrieve(target_persona, focal_points, 15)
    
    print('\n-------------------- target new retrieved for convo ---------------------: \n', retrieved)
    for key, val in retrieved.items():
      print("'", key, "': ")
      for i in val:
        print(i.type, " / ", i.spo_summary())
    print("-------------------------------------------------------------------------\n")
    
    utt, end = generate_one_utterance(target_persona, init_persona, retrieved, curr_chat)
    #utt, end = generate_one_utterance(target_persona, init_persona, curr_chat)

    curr_chat += [[target_persona.scratch.name, utt]]
    if end:
      break

  print ("July 23 PU")
  for row in curr_chat: 
    print (row)
  print ("July 23 FIN")

  return curr_chat


def agent_with_user_chat(init_persona):
  curr_chat = []
  print ("July 23")
  for i in range(2): 
    # focal_points = [f"{target_persona.scratch.name}"]
    # print("focal_points: ", focal_points)
    # retrieved = new_retrieve(init_persona, focal_points, 50)
    
    # print('\n--------------- retrieved for convo ----------------: \n', retrieved)
    # for key, val in retrieved.items():
    #   print("'", key, "': ")
    #   for i in val:
    #     print(i.type, " / ", i.spo_summary())
    # print("----------------------------------------------------\n")
    
    # relationship = generate_summarize_agent_relationship(init_persona, target_persona, retrieved)
    # print ("-------- relationship", relationship)
    # last_chat = ""
    # for i in curr_chat[-4:]:
    #   last_chat += ": ".join(i) + "\n"
    # if last_chat: 
    #   focal_points = [f"{relationship}", 
    #                   f"{target_persona.scratch.name} is {target_persona.scratch.act_description}", 
    #                   last_chat]
    # else: 
    #   focal_points = [f"{relationship}", 
    #                   f"{target_persona.scratch.name} is {target_persona.scratch.act_description}"]
    # print("new focal_points: ", focal_points)
    # retrieved = new_retrieve(init_persona, focal_points, 15)
    
    # print('\n------------------ new retrieved for convo --------------------: \n', retrieved)
    # for key, val in retrieved.items():
    #   print("'", key, "': ")
    #   for i in val:
    #     print(i.type, " / ", i.spo_summary())
    # print("---------------------------------------------------------------\n")
    
    utt, end = generate_one_utterance(init_persona, None, None, curr_chat)
    #utt, end = generate_one_utterance(init_persona, target_persona, curr_chat)

    curr_chat += [[init_persona.scratch.name, utt]]
    # if end:
    #   break
    
    user_chat = input("대화를 입력하세요: ")
    curr_chat += [["User", user_chat]]
    
  curr_chat += [[init_persona.scratch.name, "그럼 저는 이만 가보겠습니다"]]
  return curr_chat


#api로 메세지 받아서 반환하는 함수.
def agent_with_user_chat_api(init_persona,message,round,reliability):
  round = int(round) 
  if round != -1 and init_persona.scratch.chatting_with != None and init_persona.scratch.chatting_with != "User" :
      utt = init_persona.scratch.chatting_with + "와 대화 중. 대화가 불가능한 상태입니다."
      end = True
      return utt, end

  # 신뢰도 5 이하일 때 : 글자 수 제한(10자 이하), 대화 3회
  # 신뢰도 6~15 일때 : 글자 수 40자, 대화 6회
  # 신뢰도 30 이하일 때 : 최대 8회 

  if reliability <= 5:
        max_round = 3
  elif reliability <= 15:
        max_round = 6
  elif reliability >= 30:
        max_round = 8
  else:
        max_round = 3  
  init_persona.scratch.chatting_with = "User"
  curr_chat = []
  if round != -1 :
    curr_chat = init_persona.scratch.chat
  else : 
     init_persona.scratch.act_description = ""
  
  if round <= max_round : 
    # focal_points = [f"{target_persona.scratch.name}"]
    # print("focal_points: ", focal_points)
    # retrieved = new_retrieve(init_persona, focal_points, 50)
    
    # print('\n--------------- retrieved for convo ----------------: \n', retrieved)
    # for key, val in retrieved.items():
    #   print("'", key, "': ")
    #   for i in val:
    #     print(i.type, " / ", i.spo_summary())
    # print("----------------------------------------------------\n")
    
    # relationship = generate_summarize_agent_relationship(init_persona, target_persona, retrieved)
    # print ("-------- relationship", relationship)
    # last_chat = ""
    # for i in curr_chat[-4:]:
    #   last_chat += ": ".join(i) + "\n"
    # if last_chat: 
    #   focal_points = [f"{relationship}", 
    #                   f"{target_persona.scratch.name} is {target_persona.scratch.act_description}", 
    #                   last_chat]
    # else: 
    #   focal_points = [f"{relationship}", 
    #                   f"{target_persona.scratch.name} is {target_persona.scratch.act_description}"]
    # print("new focal_points: ", focal_points)
    # retrieved = new_retrieve(init_persona, focal_points, 15)
    
    # print('\n------------------ new retrieved for convo --------------------: \n', retrieved)
    # for key, val in retrieved.items():
    #   print("'", key, "': ")
    #   for i in val:
    #     print(i.type, " / ", i.spo_summary())
    # print("---------------------------------------------------------------\n")
    
    if round != 0:
      curr_chat += [["User", message]]

    print("---------------------------------------------")
    print(curr_chat)
    utt, end = generate_one_utterance(init_persona, None, None, curr_chat)
    #utt, end = generate_one_utterance(init_persona, target_persona, curr_chat)

    if end or round == max_round:
      end = True
      init_persona.scratch.chatting_with = None
      utt += "그럼 저는 이만 가보겠습니다."

    curr_chat += [[init_persona.scratch.name, utt]]
    init_persona.scratch.chat = curr_chat
      
    
  return utt, end
      
    
def generate_summarize_ideas(persona, nodes, question): 
  statements = ""
  for n in nodes:
    statements += f"{n.embedding_key}\n"
  summarized_idea = run_gpt_prompt_summarize_ideas(persona, statements, question)[0]
  return summarized_idea


def generate_next_line(persona, interlocutor_desc, curr_convo, summarized_idea):
  # Original chat -- line by line generation 
  prev_convo = ""
  for row in curr_convo: 
    prev_convo += f'{row[0]}: {row[1]}\n'

  next_line = run_gpt_prompt_generate_next_convo_line(persona, 
                                                      interlocutor_desc, 
                                                      prev_convo, 
                                                      summarized_idea)[0]  
  return next_line


def generate_inner_thought(persona, whisper):
  inner_thought = run_gpt_prompt_generate_whisper_inner_thought(persona, whisper)[0]
  return inner_thought

def generate_action_event_triple(act_desp, persona): 
  """TODO 

  INPUT: 
    act_desp: the description of the action (e.g., "sleeping")
    persona: The Persona class instance
  OUTPUT: 
    a string of emoji that translates action description.
  EXAMPLE OUTPUT: 
    "🧈🍞"
  """
  if debug: print ("GNS FUNCTION: <generate_action_event_triple>")
  return run_gpt_prompt_event_triple(act_desp, persona)[0]


def generate_poig_score(persona, event_type, description): 
  if debug: print ("GNS FUNCTION: <generate_poig_score>")

  if "is idle" in description: 
    return 1

  if event_type == "event" or event_type == "thought": 
    return run_gpt_prompt_event_poignancy(persona, description)[0]
  elif event_type == "chat": 
    return run_gpt_prompt_chat_poignancy(persona, 
                           persona.scratch.act_description)[0]


def load_history_via_whisper(personas, whispers):
  for count, row in enumerate(whispers): 
    persona = personas[row[0]]
    whisper = row[1]

    thought = generate_inner_thought(persona, whisper)

    created = persona.scratch.curr_time
    expiration = persona.scratch.curr_time + datetime.timedelta(days=30)
    s, p, o = generate_action_event_triple(thought, persona)
    keywords = set([s, p, o])
    thought_poignancy = generate_poig_score(persona, "event", whisper)
    thought_embedding_pair = (thought, get_embedding(thought))
    persona.a_mem.add_thought(created, expiration, s, p, o, 
                              thought, keywords, thought_poignancy, 
                              thought_embedding_pair, None)


def open_convo_session(persona, convo_mode): 
  if convo_mode == "analysis": 
    curr_convo = []
    interlocutor_desc = "Interviewer"

    while True: 
      line = input("Enter Input: ")
      if line == "end_convo": 
        break

      if int(run_gpt_generate_safety_score(persona, line)[0]) >= 8: 
        print (f"{persona.scratch.name} is a computational agent, and as such, it may be inappropriate to attribute human agency to the agent in your communication.")        

      else: 
        retrieved = new_retrieve(persona, [line], 50)[line]
        summarized_idea = generate_summarize_ideas(persona, retrieved, line)
        curr_convo += [[interlocutor_desc, line]]

        next_line = generate_next_line(persona, interlocutor_desc, curr_convo, summarized_idea)
        curr_convo += [[persona.scratch.name, next_line]]


  elif convo_mode == "whisper": 
    whisper = input("Enter Input: ")
    thought = generate_inner_thought(persona, whisper)

    created = persona.scratch.curr_time
    expiration = persona.scratch.curr_time + datetime.timedelta(days=30)
    s, p, o = generate_action_event_triple(thought, persona)
    keywords = set([s, p, o])
    thought_poignancy = generate_poig_score(persona, "event", whisper)
    thought_embedding_pair = (thought, get_embedding(thought))
    persona.a_mem.add_thought(created, expiration, s, p, o, 
                              thought, keywords, thought_poignancy, 
                              thought_embedding_pair, None)
































