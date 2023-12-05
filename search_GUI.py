import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class PatentSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Patent Search')

        layout = QVBoxLayout()

        label = QLabel('직업을 입력하세요:')
        self.job_input = QLineEdit()
        layout.addWidget(label)
        layout.addWidget(self.job_input)

        search_button = QPushButton('검색')
        search_button.clicked.connect(self.search_patents)
        layout.addWidget(search_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.show()

    def search_patents(self):
        job = self.job_input.text()  # 입력된 직업
        # 여기에 직업과 관련된 특허 검색 및 결과 출력하는 코드 추가
        similar_patents = self.find_similar_patents(job)
        
        if similar_patents:
            result_text = "\n".join(similar_patents)
        else:
            result_text = "일치하는 특허를 찾지 못했습니다."
        
        self.result_label.setText(result_text)

    def find_similar_patents(self, job):
        # 여기에 직업과 관련된 특허 검색하는 코드를 작성해야 합니다.
        # 입력된 직업과 유사한 특허를 찾아 반환하는 로직을 구현해야 합니다.
        # (여기서는 실제 데이터가 없으므로 가상의 로직으로 대체하였습니다.)
        if job == "engineer":
            return [
                "특허 1: 엔진 개발에 관한 내용입니다.",
                "특허 2: 공학 분야의 특허입니다."
            ]
        elif job == "scientist":
            return [
                "특허 3: 과학 연구 관련 특허입니다.",
                "특허 4: 신기술 발견에 관한 특허입니다."
            ]
        else:
            return []


def main():
    app = QApplication(sys.argv)
    patent_search_app = PatentSearchApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
