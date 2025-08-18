import os


def list_data_files(data_folder):
    pdfs, excels = [], []
    for fname in os.listdir(data_folder):
        fpath = os.path.join(data_folder, fname)
        if fname.lower().endswith(".pdf"):
            pdfs.append(fpath)
        elif fname.lower().endswith((".xls", ".xlsx")):
            excels.append(fpath)
    return pdfs, excels
