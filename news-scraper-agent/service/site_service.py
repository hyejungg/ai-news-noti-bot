from models import Site
from graph import State

# site 정보를 가져와 node 의 상태 중 하나로 추가
def get_sites(state: State) -> State:
    sites = list(Site.objects(verified=True))  # QuerySet을 리스트로 변환
    print(f"sites: {sites}")

    # 새로운 딕셔너리를 생성하여 기존 상태를 복사하고 sites를 추가
    new_state = dict(state)
    new_state["sites"] = sites

    return new_state
