#include <iostream>
#include <vector>
#include <limits>

using namespace std;

class Button {
    public:
        virtual ~Button() = default;
        virtual void push(){;}
};

class HypeButton : public Button {
    public:
        virtual void push() {
            cout << "HYPE HYPE HYPE" << endl;
        }
};

class WinnerButton : public Button {
    public:
        virtual void push() {
            cout << "WINNER WINNER WINNER" << endl;
            system("/bin/sh");
        }
};

class CustomButton : public Button {
    public:
        CustomButton() {
            cout << "Enter the name for your custom button!" << endl;
            scanf("%s", name);
        }
        virtual void push() {
            cout << name << " " << name << " " << name << endl;
        }
    private:
        char name[0x10];
};

class Application {
public:
    Application() {
        cout << "We have great buttons, try your hand!" << endl;
    }

    void run() {
        int choice = 0;
        while (true) {
            displayMenu();

            if (!(std::cin >> choice)) {
                std::cout << "\nInvalid input. Please enter a number (1-2).\n";

                std::cin.clear();

                clearInputBuffer();
                continue;
            }

            clearInputBuffer();
    
            std::cout << "----------------------------------------\n";

            switch (choice) {
                case 1: makeButton(); break;
                case 2: pushButton(); break;
                case 3: exit(0); break;
                default:
                    std::cout << "Option " << choice << " is not valid. Please choose from 1 to 6.\n";
                    break;
            }
            std::cout << "----------------------------------------\n\n";
        }
    }
private:
    vector<Button*> button_list;
    int button_count;

    void displayMenu() {
        cout << "What would you like to do?" << endl;
        cout << "    1. Make a new button" << endl;
        cout << "    2. Push a button" << endl;
        cout << "    3. Exit" << endl;
        cout << ">> ";
    }

    void clearInputBuffer() {
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }

    void makeButton() {
        int choice;
        bool valid;
        if (button_count > 10) {
            cout << "You can only make 10 buttons on the free trial, sorry" << endl;
            cout << "You can probably pay Macen to let you make more" << endl;
            exit(0);
        }
        cout << "What kind of button would you like to make?" << endl;
        cout << "    1. Hype Button" << endl << "    2. Custom Button" << endl << "    3. Winner Button" << endl;
        cout << ">> ";
        do {
            std::cout << "Enter your choice (1-3): ";
            
            if (!(std::cin >> choice)) {
                std::cout << "\nInvalid input type. Please enter a number (1-3).\n";
                std::cin.clear();
                clearInputBuffer();
            } else if (choice < 1 || choice > 3) {
                std::cout << "\nChoice out of range. Please enter a number (1-3).\n";
                std::cin.clear();
                clearInputBuffer();
            } else {
                valid = true;
            }
        } while (!valid);
        clearInputBuffer();

        switch (choice) {
            case 1: {
                button_list.push_back(new HypeButton());
                button_count++;
                cout << "Created a Hype Button" << endl;
            }; break;
            case 2: {
                button_list.push_back(new CustomButton());
                button_count++;
                cout << "Created a Custom Button" << endl;
            }; break;
            case 3: {
                cout << "Winner Buttons are for actual Winners... that's not you quite yet, but keep working at it" << endl;
            }; break;
            default: break;
        };
    }

    void pushButton() {
        int choice;
        bool isValid = false;
        do {
            std::cout << "You currently have " << button_count << " buttons. Pick one of them (1-" << button_count << ")" << endl;
            std::cout << ">> ";

            if (!(std::cin >> choice)) {
                std::cout << ">>> ERROR: Invalid input type. Please enter a whole number.\n";
                std::cin.clear();
                clearInputBuffer();
            } else if (choice >= button_count+1) {
                std::cout << ">>> ERROR: Input must be less than " << button_count+1 << ".\n";
                std::cin.clear();
                clearInputBuffer();
            } else {
                isValid = true;
                clearInputBuffer();
            }
            
        } while (!isValid); // Loop until the stream is good and input is valid
        button_list[choice-1]->push();
    }
};

int main() {
    WinnerButton *but = new WinnerButton();
    Application *app = new Application();
    app->run();
    return 0;
}