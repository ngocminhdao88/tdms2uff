from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from counter import Counter

counter = Counter(0, 5)

def main():
    app = QApplication([])

    widget = QWidget()
    button = QPushButton("Increase")
    button_2 = QPushButton("Reset")
    label = QLabel("Counter")

    layout = QVBoxLayout(widget)
    layout.addWidget(label)
    layout.addWidget(button)
    layout.addWidget(button_2)

    machine = QStateMachine()

    idleState = QState(machine)
    idleState.assignProperty(label, "text", "idle")
    workingState = QState(machine)
    workingState.assignProperty(label, "text", "working")

    idleToWorkingTransition = QSignalTransition(counter.started)
    idleToWorkingTransition.setTargetState(workingState)
    workingToIdleTransition = QSignalTransition(counter.tripped)
    workingToIdleTransition.setTargetState(idleState)

    idleState.addTransition(idleToWorkingTransition)
    workingState.addTransition(workingToIdleTransition)

    machine.setInitialState(idleState)
    machine.start()

    widget.show()

    button.clicked.connect(increase)
    button_2.clicked.connect(reset)

    app.exec_()

@pyqtSlot()
def increase():
    counter.countUp()
    print(counter.counter())

def reset():
    counter.reset()

if __name__ == "__main__":
    main()

