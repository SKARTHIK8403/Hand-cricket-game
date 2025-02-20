'''import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import messagebox
import random
import threading

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

class HandCricketGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Cricket Game")
        self.root.geometry("600x400")
        
        self.user_score = 0
        self.computer_score = 0
        self.target = None
        self.batting = None
        self.timer = None
        
        self.create_ui()
    
    def create_ui(self):
        tk.Label(self.root, text="Welcome to Hand Cricket!", font=("Arial", 16)).pack(pady=10)
        self.score_label = tk.Label(self.root, text=f"User: 0  |  Computer: 0", font=("Arial", 14))
        self.score_label.pack(pady=5)
        
        self.status_label = tk.Label(self.root, text="Choose Bat or Bowl", font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        tk.Button(self.root, text="Bat", command=lambda: self.start_game("bat"), width=10, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Bowl", command=lambda: self.start_game("bowl"), width=10, font=("Arial", 12)).pack(pady=5)
    
    def start_game(self, choice):
        self.batting = "user" if choice == "bat" else "computer"
        self.status_label.config(text=f"You chose to {choice}. Game starts!")
        self.play_turn()
    
    def detect_fingers(self):
        cap = cv2.VideoCapture(0)
        hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        
        finger_count = None
        
        for _ in range(30):  # Give user 3 seconds to show hand
            ret, frame = cap.read()
            if not ret:
                continue
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)
            
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    landmarks = hand_landmarks.landmark
                    tips = [4, 8, 12, 16, 20]
                    count = sum(1 for tip in tips if landmarks[tip].y < landmarks[tip - 2].y)
                    finger_count = count
            
            cv2.imshow("Hand Cricket", frame)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return finger_count if finger_count else "Invalid"
    
    def play_turn(self):
        user_move = self.detect_fingers()
        computer_move = random.randint(1, 6)
        
        if user_move == "Invalid":
            self.status_label.config(text="Invalid Move! Try again.")
            self.play_turn()
            return
        
        self.status_label.config(text=f"You: {user_move} | Computer: {computer_move}")
        
        if self.batting == "user":
            if user_move == computer_move:
                self.status_label.config(text="OUT! Now computer bats.")
                self.batting = "computer"
                self.target = self.user_score
            else:
                self.user_score += user_move
        else:
            if user_move == computer_move:
                self.status_label.config(text="Computer is OUT! Game Over.")
                winner = "You Win!" if self.user_score > self.computer_score else "Computer Wins!"
                messagebox.showinfo("Game Over", winner)
                self.root.quit()
            else:
                self.computer_score += computer_move
                if self.target and self.computer_score > self.target:
                    messagebox.showinfo("Game Over", "Computer Wins!")
                    self.root.quit()
        
        self.score_label.config(text=f"User: {self.user_score}  |  Computer: {self.computer_score}")
        self.root.after(1000, self.play_turn)
    
if __name__ == "__main__":
    root = tk.Tk()
    game = HandCricketGame(root)
    root.mainloop()'''


#Game with basic GUI
'''import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import messagebox
import random
import threading
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

class HandCricketGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Cricket Game")
        self.root.geometry("600x400")
        
        self.user_score = 0
        self.computer_score = 0
        self.target = None
        self.batting = None
        self.timer_seconds = 3  # Countdown timer

        self.create_ui()
    
    def create_ui(self):
        tk.Label(self.root, text="🏏 Welcome to Hand Cricket!", font=("Arial", 16)).pack(pady=10)

        self.score_label = tk.Label(self.root, text=f"User: 0  |  Computer: 0", font=("Arial", 14))
        self.score_label.pack(pady=5)

        self.timer_label = tk.Label(self.root, text=f"Time Left: {self.timer_seconds}s", font=("Arial", 14), fg="red")
        self.timer_label.pack(pady=5)

        self.status_label = tk.Label(self.root, text="Choose Bat or Bowl", font=("Arial", 12))
        self.status_label.pack(pady=5)

        tk.Button(self.root, text="Bat", command=lambda: self.start_game("bat"), width=10, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Bowl", command=lambda: self.start_game("bowl"), width=10, font=("Arial", 12)).pack(pady=5)

    def start_game(self, choice):
        self.batting = "user" if choice == "bat" else "computer"
        self.status_label.config(text=f"You chose to {choice}. Game starts!")
        self.play_turn()

    def countdown_timer(self):
        """Runs a countdown from 3 seconds and updates the timer label."""
        for i in range(self.timer_seconds, 0, -1):
            self.timer_label.config(text=f"Time Left: {i}s")
            time.sleep(1)
        self.timer_label.config(text="Time Left: 0s")

    def detect_fingers(self):
        """Detects fingers within a set time limit using Mediapipe."""
        cap = cv2.VideoCapture(0)
        hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        
        start_time = time.time()
        finger_count = None

        while time.time() - start_time < self.timer_seconds:
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    landmarks = hand_landmarks.landmark
                    tips = [4, 8, 12, 16, 20]
                    count = sum(1 for tip in tips if landmarks[tip].y < landmarks[tip - 2].y)
                    finger_count = count

            cv2.imshow("Hand Cricket - Show Your Move", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return finger_count if finger_count else "Invalid"

    def play_turn(self):
        """Manages game logic for turns."""
        self.timer_label.config(text=f"Time Left: {self.timer_seconds}s")
        
        timer_thread = threading.Thread(target=self.countdown_timer)
        timer_thread.start()

        user_move = self.detect_fingers()
        computer_move = random.randint(1, 6)

        if user_move == "Invalid":
            self.status_label.config(text="⏳ Time Up! Invalid Move. Try again.")
            self.play_turn()
            return

        self.status_label.config(text=f"You: {user_move} | Computer: {computer_move}")

        if self.batting == "user":
            if user_move == computer_move:
                self.status_label.config(text="OUT! Now computer bats.")
                self.batting = "computer"
                self.target = self.user_score + 1
            else:
                self.user_score += user_move
        else:
            if user_move == computer_move:
                self.status_label.config(text="Computer is OUT! Game Over.")
                winner = "🎉 You Win!" if self.user_score > self.computer_score else "🤖 Computer Wins!"
                messagebox.showinfo("Game Over", winner)
                self.root.quit()
            else:
                self.computer_score += computer_move
                if self.target and self.computer_score >= self.target:
                    messagebox.showinfo("Game Over", "🤖 Computer Wins!")
                    self.root.quit()

        self.score_label.config(text=f"User: {self.user_score}  |  Computer: {self.computer_score}")
        self.root.after(1000, self.play_turn)

if __name__ == "__main__":
    root = tk.Tk()
    game = HandCricketGame(root)
    root.mainloop()'''

#Game with better GUI
'''import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import messagebox, ttk
import random
import threading
import time
import pygame

# Initialize pygame for sound effects
pygame.mixer.init()

# Load sound effects
sound_score = pygame.mixer.Sound("sounds/score.wav")   # Play on scoring
sound_out = pygame.mixer.Sound("sounds/score.wav")       # Play when OUT

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

class HandCricketGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Cricket Game")
        self.root.geometry("700x500")
        self.root.configure(bg="lightblue")

        self.user_score = 0
        self.computer_score = 0
        self.target = None
        self.batting = None
        self.history = []
        self.timer = None
        self.time_left = 4  # Time limit for each move

        self.create_ui()
    
    def create_ui(self):
        tk.Label(self.root, text="🏏 Hand Cricket Game 🏏", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=10)
        self.score_label = tk.Label(self.root, text=f"User: 0  |  Computer: 0", font=("Arial", 14), bg="lightblue")
        self.score_label.pack(pady=5)

        # Timer label
        self.timer_label = tk.Label(self.root, text="Time left: 4s", font=("Arial", 14, "bold"), fg="red", bg="lightblue")
        self.timer_label.pack()

        self.status_label = tk.Label(self.root, text="Choose Bat or Bowl", font=("Arial", 12), bg="lightblue")
        self.status_label.pack(pady=5)

        tk.Button(self.root, text="Bat", command=lambda: self.start_game("bat"), width=10, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Bowl", command=lambda: self.start_game("bowl"), width=10, font=("Arial", 12)).pack(pady=5)

        # Game history table
        self.history_table = ttk.Treeview(self.root, columns=("User", "Computer"), show="headings")
        self.history_table.heading("User", text="User Move")
        self.history_table.heading("Computer", text="Computer Move")
        self.history_table.pack(pady=10)

    def start_game(self, choice):
        self.batting = "user" if choice == "bat" else "computer"
        self.status_label.config(text=f"You chose to {choice}. Game starts!")
        self.play_turn()

    def detect_fingers(self):
        cap = cv2.VideoCapture(0)
        hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        finger_count = None
        self.time_left = 4  # Reset timer

        while self.time_left > 0:
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    landmarks = hand_landmarks.landmark
                    tips = [4, 8, 12, 16, 20]
                    count = sum(1 for tip in tips if landmarks[tip].y < landmarks[tip - 2].y)
                    finger_count = count

            # Update timer
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.root.update()

            cv2.imshow("Hand Cricket", frame)
            if cv2.waitKey(1000) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return finger_count if finger_count else "Invalid"

    def play_turn(self):
        self.time_left = 4  # Reset timer for new turn
        self.timer_label.config(text=f"Time left: {self.time_left}s")

        user_move = self.detect_fingers()
        computer_move = random.randint(1, 6)

        if user_move == "Invalid":
            self.status_label.config(text="⏳ Invalid Move! Try again.")
            self.play_turn()
            return

        self.status_label.config(text=f"You: {user_move} | Computer: {computer_move}")

        if self.batting == "user":
            if user_move == computer_move:
                self.status_label.config(text="🚨 OUT! Now computer bats.")
                sound_out.play()
                self.batting = "computer"
                self.target = self.user_score
            else:
                self.user_score += user_move
                sound_score.play()
        else:
            if user_move == computer_move:
                self.status_label.config(text="🚨 Computer is OUT! Game Over.")
                sound_out.play()
                winner = "🎉 You Win!" if self.user_score > self.computer_score else "😢 Computer Wins!"
                messagebox.showinfo("Game Over", winner)
                self.root.quit()
            else:
                self.computer_score += computer_move
                sound_score.play()
                if self.target and self.computer_score > self.target:
                    messagebox.showinfo("Game Over", "😢 Computer Wins!")
                    self.root.quit()

        # Update score and history
        self.score_label.config(text=f"User: {self.user_score}  |  Computer: {self.computer_score}")
        self.history.append((user_move, computer_move))
        self.history_table.insert("", "end", values=(user_move, computer_move))

        self.root.after(1000, self.play_turn)

if __name__ == "__main__":
    root = tk.Tk()
    game = HandCricketGame(root)
    root.mainloop()'''

#Game with proper logic
'''import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import messagebox, ttk
import random
import threading
import time
import pygame

# Initialize pygame for sound effects
pygame.mixer.init()

# Load sound effects
sound_score = pygame.mixer.Sound("sounds/score.wav")   # Play on scoring
sound_out = pygame.mixer.Sound("sounds/score.wav")       # Play when OUT

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

class HandCricketGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Cricket Game")
        self.root.geometry("700x500")
        self.root.configure(bg="lightblue")

        self.user_score = 0
        self.computer_score = 0
        self.target = None
        self.batting = None
        self.history = []
        self.time_left = 4  # Time limit for each move

        self.create_ui()
    
    def create_ui(self):
        tk.Label(self.root, text="🏏 Hand Cricket Game 🏏", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=10)
        self.score_label = tk.Label(self.root, text=f"User: 0  |  Computer: 0", font=("Arial", 14), bg="lightblue")
        self.score_label.pack(pady=5)

        # Timer label
        self.timer_label = tk.Label(self.root, text="Time left: 4s", font=("Arial", 14, "bold"), fg="red", bg="lightblue")
        self.timer_label.pack()

        self.status_label = tk.Label(self.root, text="Choose Bat or Bowl", font=("Arial", 12), bg="lightblue")
        self.status_label.pack(pady=5)

        tk.Button(self.root, text="Bat", command=lambda: self.start_game("bat"), width=10, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Bowl", command=lambda: self.start_game("bowl"), width=10, font=("Arial", 12)).pack(pady=5)

        # Game history table
        self.history_table = ttk.Treeview(self.root, columns=("User", "Computer"), show="headings")
        self.history_table.heading("User", text="User Move")
        self.history_table.heading("Computer", text="Computer Move")
        self.history_table.pack(pady=10)

    def start_game(self, choice):
        """Starts the game with user choice (Bat or Bowl)."""
        self.batting = "user" if choice == "bat" else "computer"
        self.status_label.config(text=f"You chose to {choice}. Game starts!")
        self.play_turn()

    def detect_fingers(self):
        """Detects fingers within a set time limit using Mediapipe."""
        cap = cv2.VideoCapture(0)
        hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        start_time = time.time()
        finger_count = None

        while time.time() - start_time < 4:  # Timer for 4 seconds
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    landmarks = hand_landmarks.landmark
                    tips = [4, 8, 12, 16, 20]
                    count = sum(1 for tip in tips if landmarks[tip].y < landmarks[tip - 2].y)
                    finger_count = count

            cv2.imshow("Hand Cricket - Show Your Move", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return finger_count if finger_count else "Invalid"

    def play_turn(self):
        """Handles the logic for playing a turn."""
        self.timer_label.config(text="Time left: 4s")

        user_move = self.detect_fingers()
        computer_move = random.randint(1, 6)

        if user_move == "Invalid":
            self.status_label.config(text="⏳ Invalid Move! Try again.")
            self.play_turn()
            return

        self.status_label.config(text=f"You: {user_move} | Computer: {computer_move}")

        if self.batting == "user":
            if user_move == computer_move:
                self.status_label.config(text="🚨 OUT! Now computer bats.")
                sound_out.play()
                self.batting = "computer"
                self.target = self.user_score + 1  # Set target for computer
            else:
                self.user_score += user_move
                sound_score.play()

        else:  # Computer batting
            if user_move == computer_move:
                self.status_label.config(text="🚨 Computer is OUT!")
                sound_out.play()

                if self.target is None:  
                    self.status_label.config(text="Now you chase the target!")
                    self.batting = "user"
                    self.target = self.computer_score + 1
                    return
                else:
                    self.declare_winner()
                    return

            else:
                self.computer_score += computer_move
                sound_score.play()
                
                if self.target and self.computer_score >= self.target:
                    self.declare_winner()
                    return

        # Update score and history
        self.score_label.config(text=f"User: {self.user_score}  |  Computer: {self.computer_score}")
        self.history.append((user_move, computer_move))
        self.history_table.insert("", "end", values=(user_move, computer_move))

        self.root.after(1000, self.play_turn)

    def declare_winner(self):
        """Declares the winner and exits the game."""
        winner = "🎉 You Win!" if self.user_score > self.computer_score else "😢 Computer Wins!"
        messagebox.showinfo("Game Over", winner)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = HandCricketGame(root)
    root.mainloop()
'''

#Game with correct logic#1
'''import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import pygame

pygame.mixer.init()

# Load sound effects
sound_score = pygame.mixer.Sound("sounds/score.wav")  
sound_out = pygame.mixer.Sound("sounds/score.wav")  

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

class HandCricketGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Cricket Game")
        self.root.geometry("700x500")
        self.root.configure(bg="lightblue")

        self.user_score = 0
        self.computer_score = 0
        self.target = None
        self.batting = None
        self.history = []

        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="🏏 Hand Cricket Game 🏏", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=10)
        self.score_label = tk.Label(self.root, text="User: 0  |  Computer: 0", font=("Arial", 14), bg="lightblue")
        self.score_label.pack(pady=5)

        self.status_label = tk.Label(self.root, text="Choose Bat or Bowl", font=("Arial", 12), bg="lightblue")
        self.status_label.pack(pady=5)

        tk.Button(self.root, text="Bat", command=lambda: self.start_game("bat"), width=10, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Bowl", command=lambda: self.start_game("bowl"), width=10, font=("Arial", 12)).pack(pady=5)

        self.history_table = ttk.Treeview(self.root, columns=("User", "Computer"), show="headings")
        self.history_table.heading("User", text="User Move")
        self.history_table.heading("Computer", text="Computer Move")
        self.history_table.pack(pady=10)

    def start_game(self, choice):
        """Starts the game with user choice (Bat or Bowl)."""
        self.user_score = 0
        self.computer_score = 0
        self.target = None
        self.history_table.delete(*self.history_table.get_children())  

        self.batting = "user" if choice == "bat" else "computer"
        self.status_label.config(text=f"You chose to {choice}. Game starts!")
        self.play_turn()
    
    def start_game(self, choice):
        self.user_score = 0
        self.computer_score = 0
        self.history_table.delete(*self.history_table.get_children())  
        if choice == "bat":
            self.batting = "user"
            self.target = None  # Target will be set after user gets out
        else:  # User bowls first
            self.batting = "computer"
            self.target = 0  # Set target to 0 so no comparison error occurs

        self.status_label.config(text=f"You chose to {choice}. Game starts!")
        self.play_turn()

    def detect_fingers(self):
        """Detects fingers using Mediapipe within 4 seconds."""
        cap = cv2.VideoCapture(0)
        hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        start_time = time.time()
        finger_count = None

        while time.time() - start_time < 4:  # Timer for 4 seconds
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    landmarks = hand_landmarks.landmark
                    tips = [4, 8, 12, 16, 20]
                    count = sum(1 for tip in tips if landmarks[tip].y < landmarks[tip - 2].y)
                    finger_count = count

            cv2.imshow("Hand Cricket - Show Your Move", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return finger_count if finger_count else "Invalid"

    def play_turn(self):
        """Handles the logic for playing a turn."""
        user_move = self.detect_fingers()
        computer_move = random.randint(1, 6)

        if user_move == "Invalid":
            self.status_label.config(text="⏳ Invalid Move! Try again.")
            self.play_turn()
            return

        if self.batting == "user":
            if user_move == computer_move:
                self.status_label.config(text=f"🚨 OUT! You Scored {self.user_score}. Now computer bats!")
                sound_out.play()
                self.history_table.insert("", "end", values=(user_move, computer_move), tags=("out",))
                self.batting = "computer"
                self.target = self.user_score + 1
                self.root.after(2000, self.play_turn)  # Delay before computer bats
                return
            else:
                self.user_score += user_move
                sound_score.play()
                self.history_table.insert("", "end", values=(user_move, computer_move))

        else:  # Computer batting
            if user_move == computer_move:
                self.status_label.config(text=f"🚨 Computer is OUT! It scored {self.computer_score}. You win!")
                sound_out.play()
                self.history_table.insert("", "end", values=(user_move, computer_move), tags=("out",))
                self.declare_winner("user")
                return
            else:
                self.computer_score += computer_move
                sound_score.play()
                self.history_table.insert("", "end", values=(user_move, computer_move))

                if self.computer_score >= self.target:
                    self.declare_winner("computer")
                    return

        # Update score
        self.score_label.config(text=f"User: {self.user_score}  |  Computer: {self.computer_score}")

        self.root.after(1000, self.play_turn)

    def declare_winner(self, winner):
        """Declares the winner and asks for replay."""
        if winner == "user":
            msg = "🎉 You Win!"
        else:
            msg = "😢 Computer Wins!"

        messagebox.showinfo("Game Over", msg)

        # Ask if user wants to play again
        play_again = messagebox.askyesno("Play Again", "Do you want to play again?")
        if play_again:
            self.status_label.config(text="Choose Bat or Bowl")
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = HandCricketGame(root)
    root.mainloop()
'''

import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import pygame

pygame.mixer.init()
sound_score = pygame.mixer.Sound("sounds/score.wav")  
sound_out = pygame.mixer.Sound("sounds/score.wav")      

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

class HandCricketGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Cricket Game")
        self.root.geometry("700x500")
        self.root.configure(bg="lightblue")

        self.user_score = 0
        self.computer_score = 0
        self.target = None  
        self.batting = None
        self.history = []

        self.create_ui()
    
    def create_ui(self):
        tk.Label(self.root, text="🏏 Hand Cricket Game 🏏", font=("Arial", 18, "bold"), bg="lightblue").pack(pady=10)
        self.score_label = tk.Label(self.root, text="User: 0  |  Computer: 0", font=("Arial", 14), bg="lightblue")
        self.score_label.pack(pady=5)

        self.timer_label = tk.Label(self.root, text="Time left: 4s", font=("Arial", 14, "bold"), fg="red", bg="lightblue")
        self.timer_label.pack()

        self.status_label = tk.Label(self.root, text="Choose Bat or Bowl", font=("Arial", 12), bg="lightblue")
        self.status_label.pack(pady=5)

        tk.Button(self.root, text="Bat", command=lambda: self.start_game("bat"), width=10, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Bowl", command=lambda: self.start_game("bowl"), width=10, font=("Arial", 12)).pack(pady=5)

        self.history_table = ttk.Treeview(self.root, columns=("User", "Computer", "Status"), show="headings")
        self.history_table.heading("User", text="User Move")
        self.history_table.heading("Computer", text="Computer Move")
        self.history_table.heading("Status", text="Result")
        self.history_table.pack(pady=10)

    def start_game(self, choice):
        """Starts the game with user choice (Bat or Bowl)."""
        self.user_score = 0
        self.computer_score = 0
        self.target = None  
        self.history = []
        self.history_table.delete(*self.history_table.get_children())  

        self.batting = "user" if choice == "bat" else "computer"
        self.status_label.config(text=f"You chose to {choice}. Game starts!")
        self.play_turn()

    def detect_fingers(self):
        """Detects fingers within a set time limit using Mediapipe."""
        cap = cv2.VideoCapture(0)
        hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        start_time = time.time()
        finger_count = None

        while time.time() - start_time < 4:
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    landmarks = hand_landmarks.landmark
                    tips = [4, 8, 12, 16, 20]
                    count = sum(1 for tip in tips if landmarks[tip].y < landmarks[tip - 2].y)
                    finger_count = count

            cv2.imshow("Hand Cricket - Show Your Move", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return finger_count if finger_count else "Invalid"

    def play_turn(self):
        """Handles the logic for playing a turn."""
        self.timer_label.config(text="Time left: 4s")

        user_move = self.detect_fingers()
        computer_move = random.randint(1, 5)

        if user_move == "Invalid":
            self.status_label.config(text="⏳ Invalid Move! Try again.")
            self.play_turn()
            return

        self.status_label.config(text=f"You: {user_move} | Computer: {computer_move}")

        if self.batting == "user":
            if user_move == computer_move:
                self.status_label.config(text="🚨 OUT! Now computer bats.")
                sound_out.play()
                self.target = self.user_score + 1  
                self.batting = "computer"
                self.history_table.insert("", "end", values=(user_move, computer_move, "OUT"), tags=("out",))
                self.play_turn()  # Start computer's innings
                return
            else:
                self.user_score += user_move
                sound_score.play()
                self.history_table.insert("", "end", values=(user_move, computer_move, "-"))

        else:  # Computer batting
            if user_move == computer_move:
                self.status_label.config(text="🚨 Computer is OUT! Now user chases.")
                sound_out.play()
                self.target = self.computer_score + 1  
                self.batting = "user"
                self.history_table.insert("", "end", values=(user_move, computer_move, "OUT"), tags=("out",))
                self.play_turn()  # Start user's innings
                return
            else:
                self.computer_score += computer_move
                sound_score.play()
                self.history_table.insert("", "end", values=(user_move, computer_move, "-"))
            
            if self.target is not None and self.computer_score >= self.target:
                self.declare_winner()
                return

        self.score_label.config(text=f"User: {self.user_score}  |  Computer: {self.computer_score}")

        if self.batting == "user" and (self.target is None or self.user_score < self.target):
            self.root.after(1000, self.play_turn)
        elif self.batting == "computer" and (self.target is None or self.computer_score < self.target):
            self.root.after(1000, self.play_turn)

    def declare_winner(self):
        """Declares the winner and restarts the game."""
        if self.user_score > self.computer_score:
            winner = "🎉 You Win!"
        else:
            winner = "😢 Computer Wins!"

        messagebox.showinfo("Game Over", winner)
        self.status_label.config(text="Choose Bat or Bowl to play again!")

if __name__ == "__main__":
    root = tk.Tk()
    game = HandCricketGame(root)
    root.mainloop()
