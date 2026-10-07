#!/usr/bin/env python3
"""
scripts/patch_gaussian_deck.py
Thực hiện phẫu thuật OpenXML trên Digital vs. Analog Reliable Signal Science Presentation.pptx:
1. Cập nhật Slide 1 (Bìa): Tiêu đề VAD Gaussian, Ngưỡng Bayes T*, Nhóm 14.
2. Cập nhật Slide 2 (Quy trình 4 STAGE): Chuẩn hóa nội dung 4 bước thuật toán Gaussian Bayes.
3. Cập nhật Slide 3 (Huấn luyện): Bổ sung Tiêu đề chuẩn và chú thích phân phối Gaussian, nghiệm Bayes T*.
4. Cập nhật Slide 4 (Bảng Định lượng): Thêm Tiêu đề, chèn Native PowerPoint Table 5 cột x 8 hàng và 3 kết luận.
5. Cập nhật Slide 5 (Dạng sóng & Sai số Âm học): Cập nhật 4 chú thích phân tích Err Start vs Err End.
6. Cắt tỉa Slide 6-16 và dọn dẹp quan hệ, đóng gói lại file .pptx chuẩn xác 100%.
"""

import os
import shutil
import zipfile
import re
from pathlib import Path
import xml.dom.minidom

PPTX_PATH = Path("Digital vs. Analog Reliable Signal Science Presentation.pptx")
BACKUP_PATH = Path("Digital vs. Analog Reliable Signal Science Presentation.pptx.bak")
BUILD_DIR = Path("build/unpacked_patched")

def backup_original():
    if not BACKUP_PATH.exists():
        print(f"[*] Tạo bản sao lưu gốc -> {BACKUP_PATH}")
        shutil.copy2(PPTX_PATH, BACKUP_PATH)
    else:
        print(f"[+] Bản sao lưu đã tồn tại: {BACKUP_PATH}")

def unpack_pptx():
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[*] Giải nén {BACKUP_PATH} -> {BUILD_DIR}")
    with zipfile.ZipFile(BACKUP_PATH, 'r') as z:
        z.extractall(BUILD_DIR)

def patch_slide1():
    print("[*] Cập nhật Slide 1 (Trang bìa)...")
    s1_path = BUILD_DIR / "ppt" / "slides" / "slide1.xml"
    with open(s1_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    # Cập nhật TextBox 8 thành 3 đoạn văn bản rõ ràng:
    # Đoạn 1: Tiêu đề đề tài (50pt bold, xanh cyan/blue 00A8FF)
    # Đoạn 2: Phụ đề thuật toán (28pt bold, cam F58220)
    # Đoạn 3: Tên nhóm và môn học (22pt, xám đậm 333333)
    new_textbox8 = (
        '<p:sp><p:nvSpPr><p:cNvPr name="TextBox 8" id="8"/><p:cNvSpPr txBox="true"/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm rot="0"><a:off x="2245011" y="2700000"/><a:ext cx="13797979" cy="6866388"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
        '<p:txBody><a:bodyPr anchor="t" rtlCol="false" tIns="0" lIns="0" bIns="0" rIns="0"><a:spAutoFit/></a:bodyPr><a:lstStyle/>'
        '<a:p><a:pPr algn="ctr"><a:lnSpc><a:spcPts val="7000"/></a:lnSpc></a:pPr>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="5000"><a:solidFill><a:srgbClr val="00A8FF"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>PHÂN ĐOẠN TIẾNG NÓI VÀ KHOẢNG LẶNG (VAD)</a:t></a:r></a:p>'
        '<a:p><a:pPr algn="ctr"><a:lnSpc><a:spcPts val="5000"/></a:lnSpc><a:spcBef><a:spcPts val="1500"/></a:spcBef></a:pPr>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="2800"><a:solidFill><a:srgbClr val="F58220"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>Thuật toán 3: Phân phối chuẩn Gaussian &amp; Ngưỡng Bayes T*</a:t></a:r></a:p>'
        '<a:p><a:pPr algn="ctr"><a:lnSpc><a:spcPts val="4000"/></a:lnSpc><a:spcBef><a:spcPts val="2000"/></a:spcBef></a:pPr>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="2200"><a:solidFill><a:srgbClr val="333333"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>Báo cáo Giữa kỳ môn Xử lý Tín hiệu Số (XLTHS 2026) — Nhóm 14</a:t></a:r></a:p>'
        '</p:txBody></p:sp>'
    )

    # Thay thế shape TextBox 8
    xml_content = re.sub(
        r'<p:sp><p:nvSpPr><p:cNvPr name="TextBox 8" id="8"/>.*?</p:sp>',
        new_textbox8,
        xml_content,
        flags=re.DOTALL
    )

    with open(s1_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print("    [+] Slide 1 đã được cập nhật thành công.")

def patch_slide2():
    print("[*] Cập nhật Slide 2 (Quy trình 4 STAGE)...")
    s2_path = BUILD_DIR / "ppt" / "slides" / "slide2.xml"
    dom = xml.dom.minidom.parse(str(s2_path))

    mapping = {
        'TextBox 60': ('QUY TRÌNH THUẬT TOÁN 3: PHÂN ĐOẠN GAUSSIAN BAYES', '00A8FF', '3800', True),
        'TextBox 61': ('Phân Khung & STE', '000000', '2400', True),
        'TextBox 65': ('Khung 20ms, trượt 10ms. Tính STE chuẩn hóa [0, 1].', '333333', '1800', False),
        'TextBox 62': ('Ước Lượng Gauss', '000000', '2400', True),
        'TextBox 66': ('Ước lượng tham số μ, σ cho Lặng và Tiếng nói.', '333333', '1800', False),
        'TextBox 67': ('Ngưỡng Bayes T*', '000000', '2400', True),
        'TextBox 69': ('Giải Bayes Quadratic tìm nghiệm T* = 0.002495.', '333333', '1800', False),
        'TextBox 70': ('Hậu Xử Lý & Biên', '000000', '2400', True),
        'TextBox 72': ('Khử khoảng lặng <200ms, trích xuất biên thời gian.', '333333', '1800', False),
    }

    for sp in dom.getElementsByTagName('p:sp'):
        cNvPr = sp.getElementsByTagName('p:cNvPr')
        if not cNvPr:
            continue
        name = cNvPr[0].getAttribute('name')
        if name in mapping:
            text, color, sz, bold = mapping[name]
            txBody = sp.getElementsByTagName('p:txBody')[0]
            # Xóa các paragraph cũ
            for p in list(txBody.getElementsByTagName('a:p')):
                txBody.removeChild(p)

            # Tạo paragraph mới
            new_p = dom.createElement('a:p')
            pPr = dom.createElement('a:pPr')
            pPr.setAttribute('algn', 'ctr')
            new_p.appendChild(pPr)

            r = dom.createElement('a:r')
            rPr = dom.createElement('a:rPr')
            rPr.setAttribute('lang', 'vi-VN')
            rPr.setAttribute('sz', sz)
            if bold:
                rPr.setAttribute('b', 'true')
            solidFill = dom.createElement('a:solidFill')
            srgbClr = dom.createElement('a:srgbClr')
            srgbClr.setAttribute('val', color)
            solidFill.appendChild(srgbClr)
            rPr.appendChild(solidFill)

            latin = dom.createElement('a:latin')
            latin.setAttribute('typeface', 'Arial')
            rPr.appendChild(latin)

            t = dom.createElement('a:t')
            t.appendChild(dom.createTextNode(text))

            r.appendChild(rPr)
            r.appendChild(t)
            new_p.appendChild(r)
            txBody.appendChild(new_p)

    with open(s2_path, "w", encoding="utf-8") as f:
        dom.writexml(f)
    print("    [+] Slide 2 đã được cập nhật DOM chuẩn xác.")
    print("    [+] Slide 2 đã được cập nhật thành công.")

def patch_slide3():
    print("[*] Cập nhật Slide 3 (Huấn luyện & PDF Gaussian)...")
    s3_path = BUILD_DIR / "ppt" / "slides" / "slide3.xml"
    with open(s3_path, "r", encoding="utf-8") as f:
        xml = f.read()

    # Thêm Tiêu đề Slide ở vị trí trên cùng (x=0.8", y=0.5", w=18.4", h=1.4")
    # Tọa độ EMU: x=731520, y=457200, cx=16824960, cy=1280160
    title_shape = (
        '<p:sp><p:nvSpPr><p:cNvPr name="Title 1" id="100"/><p:cNvSpPr txBox="true"/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm rot="0"><a:off x="731520" y="400000"/><a:ext cx="16824960" cy="1400000"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
        '<p:txBody><a:bodyPr anchor="t" rtlCol="false" tIns="0" lIns="0" bIns="0" rIns="0"/><a:lstStyle/>'
        '<a:p><a:pPr algn="l"/>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="3200"><a:solidFill><a:srgbClr val="00A8FF"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>HUẤN LUYỆN PHÂN BỐ GAUSSIAN &amp; NGƯỠNG TỐI ƯU T*</a:t></a:r></a:p>'
        '<a:p><a:pPr algn="l"><a:spcBef><a:spcPts val="400"/></a:spcBef></a:pPr>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="2000"><a:solidFill><a:srgbClr val="475569"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>Ước lượng tham số (μ, σ) từ 4 tệp huấn luyện và giải nghiệm Bayes Quadratic</a:t></a:r></a:p>'
        '</p:txBody></p:sp>'
    )

    # TextBox 3: Caption bên trái (Subplot a - Toàn cảnh PDF)
    new_textbox3 = (
        '<p:sp><p:nvSpPr><p:cNvPr name="TextBox 3" id="3"/><p:cNvSpPr txBox="true"/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm rot="0"><a:off x="374904" y="8073896"/><a:ext cx="8686800" cy="1800000"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
        '<p:txBody><a:bodyPr anchor="t" rtlCol="false" tIns="0" lIns="0" bIns="0" rIns="0"/><a:lstStyle/>'
        '<a:p><a:pPr algn="l"/>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="2000"><a:solidFill><a:srgbClr val="0F172A"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>• Lặng (Silence): μ = 0.00025, σ = 0.00063 (phân bố hẹp sát 0)</a:t></a:r></a:p>'
        '<a:p><a:pPr algn="l"><a:spcBef><a:spcPts val="400"/></a:spcBef></a:pPr>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="2000"><a:solidFill><a:srgbClr val="0F172A"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>• Tiếng nói (Speech): μ = 0.20247, σ = 0.23569 (phân tán rộng)</a:t></a:r></a:p>'
        '</p:txBody></p:sp>'
    )

    # TextBox 4: Caption bên phải (Subplot b - Cận cảnh giao điểm T*)
    new_textbox4 = (
        '<p:sp><p:nvSpPr><p:cNvPr name="TextBox 4" id="4"/><p:cNvSpPr txBox="true"/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm rot="0"><a:off x="9354000" y="8073896"/><a:ext cx="8800000" cy="1800000"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
        '<p:txBody><a:bodyPr anchor="t" rtlCol="false" tIns="0" lIns="0" bIns="0" rIns="0"/><a:lstStyle/>'
        '<a:p><a:pPr algn="l"/>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="2000"><a:solidFill><a:srgbClr val="F58220"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>• Nghiệm Bayes: p(x|Silence) = p(x|Speech) → T* = 0.002495</a:t></a:r></a:p>'
        '<a:p><a:pPr algn="l"><a:spcBef><a:spcPts val="400"/></a:spcBef></a:pPr>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="2000"><a:solidFill><a:srgbClr val="0F172A"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>• Điểm giao nhau tối thiểu hóa sai số phân loại nhầm</a:t></a:r></a:p>'
        '</p:txBody></p:sp>'
    )

    # Chèn title_shape vào sau <p:grpSpPr>
    xml = xml.replace('</p:grpSpPr>', f'</p:grpSpPr>{title_shape}')

    # Thay thế TextBox 3 và TextBox 4
    xml = re.sub(
        r'<p:sp><p:nvSpPr><p:cNvPr name="TextBox 3" id="3"/>.*?</p:sp>',
        new_textbox3,
        xml,
        flags=re.DOTALL
    )
    xml = re.sub(
        r'<p:sp><p:nvSpPr><p:cNvPr name="TextBox 4" id="4"/>.*?</p:sp>',
        new_textbox4,
        xml,
        flags=re.DOTALL
    )

    with open(s3_path, "w", encoding="utf-8") as f:
        f.write(xml)
    print("    [+] Slide 3 đã được cập nhật thành công.")

def patch_slide4():
    print("[*] Cập nhật Slide 4 (Bảng Định Lượng & Đánh Giá)...")
    s4_path = BUILD_DIR / "ppt" / "slides" / "slide4.xml"

    # Dữ liệu bảng thực nghiệm từ simple_statistics.ipynb
    table_data = [
        # Headers
        ("Tên Tệp", "Môi Trường", "SNR (dB)", "MAE (ms)", "RMSE (ms)"),
        # Rows
        ("phone_F2", "Phone (Nữ)", "24.8 dB", "27.5000 ms", "37.1652 ms"),
        ("phone_M2", "Phone (Nam)", "27.0 dB", "2.5000 ms", "2.5000 ms"),
        ("studio_F2", "Studio (Nữ)", "49.3 dB", "5.0000 ms", "5.5929 ms"),
        ("studio_M2", "Studio (Nam)", "37.7 dB", "12.4940 ms", "16.0031 ms"),
        # Summary Rows
        ("Trung Bình Phone", "Phone (2 tệp)", "25.9 dB", "15.0000 ms", "19.8326 ms"),
        ("Trung Bình Studio", "Studio (2 tệp)", "43.5 dB", "8.7470 ms", "10.7980 ms"),
        ("Toàn Bộ Kiểm Thử", "Overall (4 tệp)", "34.7 dB", "11.8735 ms", "15.3153 ms"),
    ]

    col_widths = [3200000, 2800000, 2600000, 3900000, 3900000] # Tổng = 16,400,000 EMU (~17.93 inches)

    # Sinh XML cho bảng
    grid_cols_xml = "".join([f'<a:gridCol w="{w}"/>' for w in col_widths])
    
    rows_xml = []
    for r_idx, row in enumerate(table_data):
        is_header = (r_idx == 0)
        is_phone_avg = (r_idx == 5)
        is_studio_avg = (r_idx == 6)
        is_overall = (r_idx == 7)
        
        # Chọn màu nền và màu chữ
        if is_header:
            bg_color = "0F172A" # Dark Slate
            txt_color = "FFFFFF"
            is_bold = "true"
            row_h = 600000
            font_sz = "2000"
        elif is_overall:
            bg_color = "0284C7" # Ocean Dark Cyan
            txt_color = "FFFFFF"
            is_bold = "true"
            row_h = 550000
            font_sz = "2000"
        elif is_phone_avg or is_studio_avg:
            bg_color = "F1F5F9" # Light Slate Gray
            txt_color = "C2410C" if is_phone_avg else "0369A1"
            is_bold = "true"
            row_h = 520000
            font_sz = "1900"
        else:
            bg_color = "FFFFFF" if (r_idx % 2 == 1) else "F8FAFC"
            txt_color = "1E293B"
            is_bold = "false"
            row_h = 500000
            font_sz = "1900"

        cells_xml = []
        for c_idx, cell_text in enumerate(row):
            # Căn lề: cột 1, 2 căn trái; cột 3, 4, 5 căn giữa/phải
            align = "l" if c_idx in [0, 1] else "ctr"
            cell_xml = (
                f'<a:tc><a:txBody><a:bodyPr anchor="ctr"/><a:lstStyle/>'
                f'<a:p><a:pPr algn="{align}"><a:buNone/></a:pPr>'
                f'<a:r><a:rPr lang="vi-VN" sz="{font_sz}" b="{is_bold}">'
                f'<a:solidFill><a:srgbClr val="{txt_color}"/></a:solidFill>'
                f'<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
                f'<a:t>{cell_text}</a:t></a:r></a:p>'
                f'</a:txBody>'
                f'<a:tcPr marL="180000" marR="180000" marT="90000" marB="90000">'
                f'<a:solidFill><a:srgbClr val="{bg_color}"/></a:solidFill>'
                f'<a:lnL w="12700"><a:solidFill><a:srgbClr val="CBD5E1"/></a:solidFill></a:lnL>'
                f'<a:lnR w="12700"><a:solidFill><a:srgbClr val="CBD5E1"/></a:solidFill></a:lnR>'
                f'<a:lnT w="12700"><a:solidFill><a:srgbClr val="CBD5E1"/></a:solidFill></a:lnT>'
                f'<a:lnB w="12700"><a:solidFill><a:srgbClr val="CBD5E1"/></a:solidFill></a:lnB>'
                f'</a:tcPr></a:tc>'
            )
            cells_xml.append(cell_xml)

        row_xml = f'<a:tr h="{row_h}">{"".join(cells_xml)}</a:tr>'
        rows_xml.append(row_xml)

    table_frame_xml = (
        '<p:graphicFrame>'
        '<p:nvGraphicFramePr><p:cNvPr id="20" name="Benchmark Table"/><p:cNvGraphicFramePr><a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr><p:nvPr/></p:nvGraphicFramePr>'
        '<p:xfrm><a:off x="914400" y="1800000"/><a:ext cx="16400000" cy="4500000"/></p:xfrm>'
        '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">'
        f'<a:tbl><a:tblPr/><a:tblGrid>{grid_cols_xml}</a:tblGrid>{"".join(rows_xml)}</a:tbl>'
        '</a:graphicData></a:graphic>'
        '</p:graphicFrame>'
    )

    # Header Slide 4
    header_shape = (
        '<p:sp><p:nvSpPr><p:cNvPr name="Title 4" id="21"/><p:cNvSpPr txBox="true"/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm rot="0"><a:off x="914400" y="400000"/><a:ext cx="16400000" cy="1300000"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
        '<p:txBody><a:bodyPr anchor="t" rtlCol="false" tIns="0" lIns="0" bIns="0" rIns="0"/><a:lstStyle/>'
        '<a:p><a:pPr algn="l"/>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="3200"><a:solidFill><a:srgbClr val="00A8FF"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>KẾT QUẢ ĐÁNH GIÁ ĐỊNH LƯỢNG TRÊN 4 TỆP KIỂM THỬ</a:t></a:r></a:p>'
        '<a:p><a:pPr algn="l"><a:spcBef><a:spcPts val="400"/></a:spcBef></a:pPr>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="2000"><a:solidFill><a:srgbClr val="475569"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>So sánh sai số biên thời gian MAE, RMSE và độ nhạy theo môi trường tạp âm</a:t></a:r></a:p>'
        '</p:txBody></p:sp>'
    )

    # Kết luận phân tích bên dưới bảng (x=1.0", y=7.4", w=17.9", h=2.8")
    takeaways_shape = (
        '<p:sp><p:nvSpPr><p:cNvPr name="Notes 4" id="22"/><p:cNvSpPr txBox="true"/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm rot="0"><a:off x="914400" y="6700000"/><a:ext cx="16400000" cy="2800000"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
        '<p:txBody><a:bodyPr anchor="t" rtlCol="false" tIns="0" lIns="0" bIns="0" rIns="0"/><a:lstStyle/>'
        '<a:p><a:pPr algn="l"/>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="2100"><a:solidFill><a:srgbClr val="0F172A"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>• Môi trường Studio (MAE 8.7ms) vượt trội rõ rệt so với Phone (MAE 15.0ms) do tỷ số SNR cao (&gt;37dB).</a:t></a:r></a:p>'
        '<a:p><a:pPr algn="l"><a:spcBef><a:spcPts val="500"/></a:spcBef></a:pPr>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="2100"><a:solidFill><a:srgbClr val="0F172A"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>• Ngưỡng Bayes T* = 0.002495 phân tách ổn định, sai số toàn bộ trung bình đạt mức rất tốt (~11.9ms).</a:t></a:r></a:p>'
        '<a:p><a:pPr algn="l"><a:spcBef><a:spcPts val="500"/></a:spcBef></a:pPr>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="2100"><a:solidFill><a:srgbClr val="C2410C"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>• Nhiễu nền kênh truyền điện thoại là tác nhân chính gây kéo dài khoảng lặng ở đuôi âm (phone_F2).</a:t></a:r></a:p>'
        '</p:txBody></p:sp>'
    )

    # Ghép toàn bộ nội dung hoàn chỉnh cho slide4.xml
    new_slide4_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<p:cSld><p:spTree>'
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        f'{header_shape}'
        f'{table_frame_xml}'
        f'{takeaways_shape}'
        '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'
    )

    with open(s4_path, "w", encoding="utf-8") as f:
        f.write(new_slide4_xml)
    print("    [+] Slide 4 đã được tạo bảng Native Table thành công.")

def patch_slide5():
    print("[*] Cập nhật Slide 5 (Dạng sóng & Phân tích Âm học)...")
    s5_path = BUILD_DIR / "ppt" / "slides" / "slide5.xml"
    with open(s5_path, "r", encoding="utf-8") as f:
        xml = f.read()

    # Thêm Tiêu đề trên cùng Slide 5
    title_shape = (
        '<p:sp><p:nvSpPr><p:cNvPr name="Title 5" id="101"/><p:cNvSpPr txBox="true"/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm rot="0"><a:off x="350000" y="100000"/><a:ext cx="17500000" cy="650000"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
        '<p:txBody><a:bodyPr anchor="t" rtlCol="false" tIns="0" lIns="0" bIns="0" rIns="0"/><a:lstStyle/>'
        '<a:p><a:pPr algn="l"/>'
        '<a:r><a:rPr lang="vi-VN" b="true" sz="2400"><a:solidFill><a:srgbClr val="00A8FF"/></a:solidFill>'
        '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
        '<a:t>DẠNG SÓNG &amp; PHÂN TÍCH NGUYÊN NHÂN SAI SỐ ÂM HỌC (4 TỆP KIỂM THỬ)</a:t></a:r></a:p>'
        '</p:txBody></p:sp>'
    )
    xml = xml.replace('</p:grpSpPr>', f'</p:grpSpPr>{title_shape}')

    # 1. TextBox 6: phone_F2 (Góc trên trái)
    # Nguyên nhân: Nhiễu nền kéo dài biên kết thúc -> Err End 52.5ms
    xml = re.sub(
        r'<p:sp><p:nvSpPr><p:cNvPr name="TextBox 6" id="6"/>.*?</p:sp>',
        (
            '<p:sp><p:nvSpPr><p:cNvPr name="TextBox 6" id="6"/><p:cNvSpPr txBox="true"/><p:nvPr/></p:nvSpPr>'
            '<p:spPr><a:xfrm rot="0"><a:off x="350000" y="4400000"/><a:ext cx="8700000" cy="750000"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
            '<p:txBody><a:bodyPr anchor="t" rtlCol="false" tIns="0" lIns="0" bIns="0" rIns="0"/><a:lstStyle/>'
            '<a:p><a:pPr algn="l"/>'
            '<a:r><a:rPr lang="vi-VN" b="true" sz="2000"><a:solidFill><a:srgbClr val="C2410C"/></a:solidFill>'
            '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
            '<a:t>• phone_F2 (Phone): Nhiễu nền kéo dài đuôi → Err End 52.5ms (MAE 27.5ms)</a:t></a:r></a:p>'
            '</p:txBody></p:sp>'
        ),
        xml,
        flags=re.DOTALL
    )

    # 2. TextBox 7: phone_M2 (Góc trên phải)
    # Nguyên nhân: Phân tách dứt khoát -> Err Start = Err End = 2.5ms
    xml = re.sub(
        r'<p:sp><p:nvSpPr><p:cNvPr name="TextBox 7" id="7"/>.*?</p:sp>',
        (
            '<p:sp><p:nvSpPr><p:cNvPr name="TextBox 7" id="7"/><p:cNvSpPr txBox="true"/><p:nvPr/></p:nvSpPr>'
            '<p:spPr><a:xfrm rot="0"><a:off x="9450000" y="4400000"/><a:ext cx="8700000" cy="750000"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
            '<p:txBody><a:bodyPr anchor="t" rtlCol="false" tIns="0" lIns="0" bIns="0" rIns="0"/><a:lstStyle/>'
            '<a:p><a:pPr algn="l"/>'
            '<a:r><a:rPr lang="vi-VN" b="true" sz="2000"><a:solidFill><a:srgbClr val="0284C7"/></a:solidFill>'
            '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
            '<a:t>• phone_M2 (Phone): Phân tách dứt khoát → Err Start=End 2.5ms (MAE 2.5ms)</a:t></a:r></a:p>'
            '</p:txBody></p:sp>'
        ),
        xml,
        flags=re.DOTALL
    )

    # 3. TextBox 8: studio_F2 (Góc dưới trái)
    # Nguyên nhân: SNR cao 49dB, bám sát chuẩn -> MAE 5.0ms
    xml = re.sub(
        r'<p:sp><p:nvSpPr><p:cNvPr name="TextBox 8" id="8"/>.*?</p:sp>',
        (
            '<p:sp><p:nvSpPr><p:cNvPr name="TextBox 8" id="8"/><p:cNvSpPr txBox="true"/><p:nvPr/></p:nvSpPr>'
            '<p:spPr><a:xfrm rot="0"><a:off x="350000" y="9600000"/><a:ext cx="8700000" cy="750000"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
            '<p:txBody><a:bodyPr anchor="t" rtlCol="false" tIns="0" lIns="0" bIns="0" rIns="0"/><a:lstStyle/>'
            '<a:p><a:pPr algn="l"/>'
            '<a:r><a:rPr lang="vi-VN" b="true" sz="2000"><a:solidFill><a:srgbClr val="0284C7"/></a:solidFill>'
            '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
            '<a:t>• studio_F2 (Studio): SNR cao 49dB, bám sát chuẩn → MAE 5.0ms (RMSE 5.6ms)</a:t></a:r></a:p>'
            '</p:txBody></p:sp>'
        ),
        xml,
        flags=re.DOTALL
    )

    # 4. TextBox 9: studio_M2 (Góc dưới phải)
    # Nguyên nhân: Trễ nhận diện bắt đầu vùng lặng giữa câu -> Err Start 22.5ms
    xml = re.sub(
        r'<p:sp><p:nvSpPr><p:cNvPr name="TextBox 9" id="9"/>.*?</p:sp>',
        (
            '<p:sp><p:nvSpPr><p:cNvPr name="TextBox 9" id="9"/><p:cNvSpPr txBox="true"/><p:nvPr/></p:nvSpPr>'
            '<p:spPr><a:xfrm rot="0"><a:off x="9450000" y="9600000"/><a:ext cx="8700000" cy="750000"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
            '<p:txBody><a:bodyPr anchor="t" rtlCol="false" tIns="0" lIns="0" bIns="0" rIns="0"/><a:lstStyle/>'
            '<a:p><a:pPr algn="l"/>'
            '<a:r><a:rPr lang="vi-VN" b="true" sz="2000"><a:solidFill><a:srgbClr val="0F172A"/></a:solidFill>'
            '<a:latin typeface="Arial"/><a:cs typeface="Arial"/></a:rPr>'
            '<a:t>• studio_M2 (Studio): Lặng giữa câu trễ bắt đầu → Err Start 22.5ms (MAE 12.5ms)</a:t></a:r></a:p>'
            '</p:txBody></p:sp>'
        ),
        xml,
        flags=re.DOTALL
    )

    with open(s5_path, "w", encoding="utf-8") as f:
        f.write(xml)
    print("    [+] Slide 5 đã được cập nhật thành công.")

def trim_slides():
    print("[*] Cắt tỉa slide thừa (Chỉ giữ đúng 5 slide đầu: rId6 -> rId10)...")
    
    # 1. Cắt tỉa ppt/presentation.xml
    pres_xml_path = BUILD_DIR / "ppt" / "presentation.xml"
    with open(pres_xml_path, "r", encoding="utf-8") as f:
        pres_xml = f.read()

    # Chỉ giữ rId6 đến rId10 trong <p:sldIdLst>
    new_sld_id_lst = (
        '<p:sldIdLst>'
        '<p:sldId id="256" r:id="rId6"/>'
        '<p:sldId id="257" r:id="rId7"/>'
        '<p:sldId id="258" r:id="rId8"/>'
        '<p:sldId id="259" r:id="rId9"/>'
        '<p:sldId id="260" r:id="rId10"/>'
        '</p:sldIdLst>'
    )
    pres_xml = re.sub(r'<p:sldIdLst>.*?</p:sldIdLst>', new_sld_id_lst, pres_xml, flags=re.DOTALL)
    with open(pres_xml_path, "w", encoding="utf-8") as f:
        f.write(pres_xml)

    # 2. Cắt tỉa ppt/_rels/presentation.xml.rels
    rels_path = BUILD_DIR / "ppt" / "_rels" / "presentation.xml.rels"
    with open(rels_path, "r", encoding="utf-8") as f:
        rels_xml = f.read()

    # Loại bỏ rId11 đến rId21 (slide6 đến slide16)
    for rid_num in range(11, 22):
        rels_xml = re.sub(rf'<Relationship[^>]*Id="rId{rid_num}"[^>]*/>', '', rels_xml)

    with open(rels_path, "w", encoding="utf-8") as f:
        f.write(rels_xml)

    # 3. Cắt tỉa [Content_Types].xml
    ct_path = BUILD_DIR / "[Content_Types].xml"
    with open(ct_path, "r", encoding="utf-8") as f:
        ct_xml = f.read()

    for s_idx in range(6, 17):
        ct_xml = re.sub(rf'<Override[^>]*PartName="/ppt/slides/slide{s_idx}\.xml"[^>]*/>', '', ct_xml)

    with open(ct_path, "w", encoding="utf-8") as f:
        f.write(ct_xml)

    # 4. Xóa các file slide6.xml -> slide16.xml và rels tương ứng
    slides_dir = BUILD_DIR / "ppt" / "slides"
    for s_idx in range(6, 17):
        s_file = slides_dir / f"slide{s_idx}.xml"
        if s_file.exists():
            s_file.unlink()
        r_file = slides_dir / "_rels" / f"slide{s_idx}.xml.rels"
        if r_file.exists():
            r_file.unlink()

    # 5. Xóa các file media không còn dùng (image23.png -> image44.svg)
    media_dir = BUILD_DIR / "ppt" / "media"
    for f in list(media_dir.glob("*")):
        m = re.match(r'image(\d+)\.', f.name)
        if m:
            img_num = int(m.group(1))
            if img_num >= 23:
                f.unlink()

    print("    [+] Đã xóa bỏ slide 6-16 và dọn dẹp quan hệ sạch sẽ.")

def repack_pptx():
    print(f"[*] Đóng gói lại tệp PPTX -> {PPTX_PATH}")
    if PPTX_PATH.exists():
        PPTX_PATH.unlink()
    
    with zipfile.ZipFile(PPTX_PATH, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(BUILD_DIR):
            for file in files:
                abs_path = Path(root) / file
                rel_path = abs_path.relative_to(BUILD_DIR)
                z.write(abs_path, rel_path)
    print(f"    [+] Hoàn tất! Kích thước file mới: {PPTX_PATH.stat().st_size / (1024*1024):.2f} MB")

def main():
    print("=== BẮT ĐẦU QUY TRÌNH PHẪU THUẬT OPENXML PPTX ===")
    backup_original()
    unpack_pptx()
    patch_slide1()
    patch_slide2()
    patch_slide3()
    patch_slide4()
    patch_slide5()
    trim_slides()
    repack_pptx()
    print("=== ĐÃ HOÀN TẤT PHẪU THUẬT OPENXML THÀNH CÔNG ===")

if __name__ == "__main__":
    main()
