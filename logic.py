from unstructured.partition.pdf import partition_pdf
import os
from pdf2image import convert_from_path

def extract_text_and_images_from_pdf(pdf_path, output_dir="extracted", use_pdf2image=False):
    # 1. 필요 시 pdf2image로 이미지 추출
    if use_pdf2image:
        try:
            images = convert_from_path(
                pdf_path,
                poppler_path="/usr/local/bin"  # 환경에 따라 "/usr/bin" 도 가능
            )
            for i, img in enumerate(images):
                img.save(os.path.join(output_dir, f"page_{i+1}.png"))
        except Exception as e:
            print("PDF2Image 변환 실패:", e)

    # 2. Unstructured로 텍스트 + 이미지 추출
    elements = partition_pdf(
        filename=pdf_path,
        extract_images_in_pdf=True,
        output_image_dir_path=output_dir
    )

    # 텍스트와 이미지 정보 분리
    texts = [el.text for el in elements if el.text]
    images = [
        el.metadata.image_path for el in elements
        if hasattr(el.metadata, 'image_path') and el.metadata.image_path
    ]

    return texts, images
