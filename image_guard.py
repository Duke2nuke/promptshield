"""Image prompt screening for PromptShield, using OpenCV.

An uploaded image is preprocessed with OpenCV (grayscale, threshold,
resize). If tesseract OCR is available, text is extracted from the
preprocessed image and screened by the same guard. If OCR is not
available, this returns unavailable instead of inventing extracted text.
"""
import io


def check_image(file_bytes):
    try:
        import cv2
        import numpy as np
    except Exception:  # noqa: BLE001
        return {"available": False, "reason": "OpenCV is not installed in this environment."}
    try:
        arr = np.frombuffer(file_bytes, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {"available": True, "error": "Could not read this image. Try a PNG or JPG file."}
        img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        _, processed = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        try:
            import pytesseract

            text = pytesseract.image_to_string(processed).strip()
        except Exception:  # noqa: BLE001
            return {"available": True, "preprocessed": True, "ocr_available": False, "note": "OpenCV preprocessing worked, but OCR (tesseract) is not available, so no text was extracted."}
        if not text:
            return {"available": True, "preprocessed": True, "ocr_available": True, "extracted_text": "", "note": "No text found in this image."}
        from guard import check_prompt

        result = check_prompt(text)
        result["extracted_text"] = text
        result["ocr_available"] = True
        return result
    except Exception as e:  # noqa: BLE001
        return {"available": True, "error": f"Image check failed: {e}"}
