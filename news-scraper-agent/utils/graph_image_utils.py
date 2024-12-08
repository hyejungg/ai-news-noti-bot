from langgraph.graph import StateGraph

from config.log import NewsScraperAgentLogger

logger = NewsScraperAgentLogger()


def get_graph_image(graph: StateGraph):
    # PNG 이미지로 그래프 그리기
    png_image = graph.get_graph().draw_mermaid_png()

    # 이미지를 파일로 저장
    with open("graph.png", "wb") as f:
        f.write(png_image)

    logger.info("Image saved as graph.png")
