from graph.state import State
from models import Site
from models.site import SiteDto


# site 정보를 가져와 node 의 상태 중 하나로 추가
def get_sites(state: State) -> State:
    site_document_list: list[Site] = list(
        Site.objects(verified=True)
    )  # QuerySet을 리스트로 변환
    sites: list[SiteDto] = [
        SiteDto(
            **{
                **site.to_mongo().to_dict(),
                "createdAt": site.createdAt or None,
                "updatedAt": site.updatedAt or None,
            }
        )
        for site in site_document_list
    ]
    print(f"sites: {sites}")

    # 기존 상태를 복사하고 sites를 추가
    new_state = state.model_copy(deep=True)
    new_state.sites = sites

    return new_state
