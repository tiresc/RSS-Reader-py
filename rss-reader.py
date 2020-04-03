import sys
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog)
class Form(QDialog):
	def __init__(self, parent=None):
		super(Form, self).__init__(parent)
		# create Widgets
		self.edit = QLineEdit("Enter RSS FEED")
		self.button = QPushButton("Enter")
		self.setWindowTitle("RSS Reader")
		# Create layout and add widgets
		layout = QVBoxLayout()
		layout.addWidget(self.edit)
		layout.addWidget(self.button)
		# Set dialog layout
		self.setLayout(layout)
		# add buton signal to greetings slot
		self.button.clicked.connect(self.greetings)

	def greetings(self):
		print ("link: {}".format(self.edit.text()))

if __name__ == '__main__':
	# Create the QT Application
	app = QApplication(sys.argv)
	# Create and show the form 
	form = Form()
	form.show()
	#Run the main QT loop
	sys.exit(app.exec_())