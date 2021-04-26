import random as rd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import math

target_error = 1e-6
root = tk.Tk()

# zmienne
W = tk.DoubleVar()
W.set(0.5)
c1 = tk.DoubleVar()
c1.set(1)
c2 = tk.DoubleVar()
c2.set(2)
n_iterations = tk.IntVar()
n_iterations.set(10)
n_particles = tk.IntVar()
n_particles.set(20)
wartoscx = tk.DoubleVar()
wartoscx.set(6)
wartoscy = tk.DoubleVar()
wartoscy.set(6)
x = int(wartoscx.get())
y = int(wartoscy.get())

# działanie przycisku
def submit():
    W.get()
    c1.get()
    c2.get()
    n_iterations.get()
    n_particles.get()
    wartoscx.get()
    wartoscy.get()
    funkcja.set(funkcja.get())
    global wynik
    if funkcja.get() == 'Sin(x) * Cos(y)':
        wynik = lambda x, y: math.sin(x) * math.cos(y)
    elif funkcja.get() == 'Funkcja Beale’a':
        wynik = lambda x, y: ((1.5 - x + x * y) ** 2) + ((2.25 - x + x * y ** 2) ** 2) + ((2.625 - x + x * y ** 3) ** 2)
    elif funkcja.get() == 'Funkcja Easoma':
        wynik = lambda x, y: -math.cos(x) * math.cos(y) * math.e ** (-(x - math.pi) ** 2 - (y - math.pi) ** 2)
    elif funkcja.get() == 'Funkcja Ackleya v2':
        wynik = lambda x, y: -200 * math.e ** (-0.2 * math.sqrt(math.pow(x, 2) + math.pow(y, 2)))
    elif funkcja.get() == 'Funkcja Himmemblau':
        wynik = lambda x, y: ((x ** 2) + y - 11) ** 2 + (x + (y ** 2) - 7) ** 2


# konfiguracja poszczególnych elementów
options = ('Sin(x) * Cos(y)',
           'Funkcja Beale’a',
           'Funkcja Easoma',
           'Funkcja Ackleya v2',
           'Funkcja Himmemblau'
           )
Inertia = tk.Label(root, text='Inertia', font=('calibre', 10, 'bold'))
Skupienienawlasnych = tk.Label(root, text='Współczynnik dążenia do najlepszego lokalnego rozwiązania',
                               font=('calibre', 10, 'bold'))
Skupienienanajlepszych = tk.Label(root, text='współczynnik dążenia do najlepszego globalnego rozwiązania',
                                  font=('calibre', 10, 'bold'))
Iteracje = tk.Label(root, text='Liczba iteracji', font=('calibre', 10, 'bold'))
iloscparticle = tk.Label(root, text='Liczba cząsteczek', font=('calibre', 10, 'bold'))
przedział = tk.Label(root, text='Przedział liczb x', font=('calibre', 10, 'bold'))
przedziała = tk.Label(root, text='Przedział liczb y', font=('calibre', 10, 'bold'))
nazwafunkcji = tk.Label(root, text='Wybór funkcji', font=('calibre', 10, 'bold'))
Entryw = tk.Entry(root, textvariable=W, font=('calibre', 10, 'normal'))
Entryc1 = tk.Entry(root, textvariable=c1, font=('calibre', 10, 'normal'))
Entryc2 = tk.Entry(root, textvariable=c2, font=('calibre', 10, 'normal'))
Entryni = tk.Entry(root, textvariable=n_iterations, font=('calibre', 10, 'normal'))
Entrynp = tk.Entry(root, textvariable=n_particles, font=('calibre', 10, 'normal'))
przedziałx = tk.Entry(root, textvariable=wartoscx, font=('calibre', 10, 'normal'))
przedziały = tk.Entry(root, textvariable=wartoscy, font=('calibre', 10, 'normal'))
Button = tk.Button(root, text='Submit', command=lambda: [submit(), root.destroy()])

# Umiejscowienie elementów w oknie
Inertia.grid(row=0, column=0)
Entryw.grid(row=0, column=1)
Skupienienawlasnych.grid(row=1, column=0)
Entryc1.grid(row=1, column=1)
Skupienienanajlepszych.grid(row=2, column=0)
Entryc2.grid(row=2, column=1)
Iteracje.grid(row=3, column=0)
Entryni.grid(row=3, column=1)
iloscparticle.grid(row=4, column=0)
Entrynp.grid(row=4, column=1)
przedział.grid(row=5, column=0)
przedziałx.grid(row=5, column=1)
przedziała.grid(row=6, column=0)
przedziały.grid(row=6, column=1)
nazwafunkcji.grid(row=7, column=0)
funkcja = ttk.Combobox(root, value=options)
funkcja.current(0)
funkcja.bind("<<ComboboxSelected>>")
funkcja.grid(row=7, column=1)
Button.grid(row=8, column=0)

# wywołanie okna oraz ustawienie wielkości
root.geometry("590x200")
root.resizable(False, False)
root.mainloop()


class Particle:

    def __init__(self):
        x = (-1) ** bool(rd.getrandbits(1)) * rd.random() * wartoscx.get()
        y = (-1) ** bool(rd.getrandbits(1)) * rd.random() * wartoscy.get()
        self.position = np.array([x, y])
        self.pBest_position = self.position
        self.pBest_value = float('inf')
        self.velocity = np.array([0, 0])

    def update(self):
        self.position = self.position + self.velocity

class Space:

    def __init__(self, target, target_error, n_particles):
        self.target = target
        self.target_error = target_error
        self.n_particles = n_particles
        self.particles = []
        self.gBest_value = float('inf')
        self.gBest_position = np.array([rd.random() * 50, rd.random() * 50])


    def fitness(self, particle):
        return wynik(particle.position[0], particle.position[1])


    def set_pBest(self):
        for particle in self.particles:
            fitness_candidate = self.fitness(particle)
            if particle.pBest_value > fitness_candidate:
                particle.pBest_value = fitness_candidate
                particle.pBest_position = particle.position

    def set_gBest(self):
        for particle in self.particles:
            best_fitness_candidate = self.fitness(particle)
            if self.gBest_value > best_fitness_candidate:
                self.gBest_value = best_fitness_candidate
                self.gBest_position = particle.position

    def update_particles(self):
        for particle in self.particles:
            global W
            inertial = W.get() * particle.velocity
            self_confidence = c1.get() * rd.random() * (particle.pBest_position - particle.position)
            swarm_confidence = c2.get() * rd.random() * (self.gBest_position - particle.position)
            new_velocity = inertial + self_confidence + swarm_confidence
            particle.velocity = new_velocity
            particle.update()

    def show_particles(self, iteration):
        print(iteration, 'iterations')

        print('Najlepsza pozycja:', self.gBest_position)
        print('Najlepsza wartość:', self.gBest_value)

        for particle in self.particles:
            print('Cząsteczka:', self.fitness(particle))
            plt.plot(particle.position[0], particle.position[1], 'ro')
        plt.plot(self.gBest_position[0], self.gBest_position[1], 'bo')
        plt.plot(x*2,y*2)
        plt.plot(-x*2,-y*2)
        plt.draw()
        plt.pause(0.5)
        plt.clf()


search_space = Space(1, target_error, n_particles.get())
particle_vector = [Particle() for _ in range(search_space.n_particles)]
search_space.particles = particle_vector

iteration = 0
while iteration < int(n_iterations.get()):
    # wyszukanie najlepszych wyników
    search_space.set_pBest()
    search_space.set_gBest()

    # wizualizacja
    search_space.show_particles(iteration)

    if abs(search_space.gBest_value - search_space.target) <= search_space.target_error:
        break
    search_space.update_particles()
    iteration += 1

print("Najlepsza solucja: ", search_space.gBest_position, " w ", iteration, " iteracjach")
