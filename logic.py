from unstructured.partition.pdf import partition_pdf
import os

def extract_text_and_images_from_pdf(pdf_path, output_dir="extracted"):
    # 추출 디렉토리 없으면 생성
    os.makedirs(output_dir, exist_ok=True)

    # Unstructured로 PDF 분할 + 이미지 추출
    elements = partition_pdf(
        filename=pdf_path,
        extract_images_in_pdf=True,
        output_image_dir_path=output_dir,
    )

    # 텍스트 요소 필터링
    texts = [el.text for el in elements if hasattr(el, 'text') and el.text]

    # 이미지 경로 필터링
    images = [
        el.metadata.image_path
        for el in elements
        if hasattr(el.metadata, 'image_path') and el.metadata.image_path
    ]

    return texts, images
