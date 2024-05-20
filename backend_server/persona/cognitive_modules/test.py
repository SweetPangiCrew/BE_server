
from pathlib import Path
import json, math

def generate_convo(init_persona, target_persona): 
  #curr_loc = maze.access_tile(init_persona.scratch.curr_tile)

  # convo = run_gpt_prompt_create_conversation(init_persona, target_persona, curr_loc)[0]
  # convo = agent_chat_v1(maze, init_persona, target_persona)

  # chat caching


    # 현재 파일의 절대 경로
    current_file_path = Path(__file__).resolve()

    # 현재 파일이 속한 디렉토리
    current_dir = current_file_path.parent

    # 상위 디렉토리
    parent_dir = current_dir.parent.parent

    # 결합할 경로
    relative_path = "storage/agenti_15/chat_caching.json"

    file_path = parent_dir / relative_path

    print(file_path)
    # JSON 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)


    if 15 >= 20 :
        desired_religious_2 = True
    else :  desired_religious_2 = False

    # 조건에 맞는 배열 찾기
    selected_chat = None
    for entry in data:
        if (entry['persona'] == "나주교" and
            entry['target_persona'] == "이화령" and
            entry['religious_2'] == desired_religious_2):
            selected_chat = entry['chat']
            break

    # 결과 출력
    if selected_chat is not None:
        print("조건에 맞는 chat 배열:", selected_chat)
        convo = selected_chat[0]

    else: #조건에 맞는 배열이 없음.
        print("없음")
        #convo = agent_chat_v2(init_persona, target_persona) #chat 대화 실시간 생성

    all_utt = ""

    for row in convo: 
        speaker = row[0]
        utt = row[1]
        all_utt += f"{speaker}: {utt}\n"
    convo_length = math.ceil(int(len(all_utt)/8) / 30)  #대화 수가 아닌 전체 대화 문장 길이로 판단

    #if debug: print ("GNS FUNCTION: <generate_convo>")
    return convo, convo_length

if __name__ == "__main__":
 generate_convo("a","b")
