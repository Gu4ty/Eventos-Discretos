import gen_rand as rand
import math
import random
import argparse

class Airport:
    def __init__(self,time_limit, verbose = False):
        self.tracks = [math.inf for _ in range(5)]
        self.t = 0
        self.cnt_q = 0
        self.track_tp = [[] for _ in range(5)]
        self.time_limit =time_limit
        self.ta = rand.exp(1/20)
        self.verbose = verbose

    def run(self):
        while(self.t < self.time_limit):
            self.t = min(self.ta, min(self.tracks))            
            if( self.ta < min(self.tracks)):
                self.arrive_plane()
            else:
                self.departure_plane()
        self.summary() 
        
    def summary(self):
        print("Track\t\tTotal Time empty")
        for i in range(5):
            plane_time = 0
            for interval in self.track_tp[i]:
                plane_time += interval[1] - interval[0]
            time_empty = self.time_limit - plane_time
            print(f'Track {i+1}:\t {time_empty} minutes')


    def arrive_plane(self):
        if max(self.tracks) < math.inf: #Trakcs are full, plane to queue
            self.cnt_q +=1
            if self.verbose:
                print("Plane arrive but in queue") 
                print(f'queue of size {self.cnt_q}')
        else: # Plane will land
            free_tracks = [i for i,j in enumerate(self.tracks) if j == math.inf]
            idx = random.choice(free_tracks)
            self.insert_plane(idx)
        self.ta = self.ta + rand.exp(1/20)

    def insert_plane(self,idx):
        td = self.calculate_time_in_airport()
        self.tracks[idx] = min(self.t + td, self.time_limit)
        self.track_tp[idx].append([self.t, self.tracks[idx]])
        if self.verbose:
            print(f'Plane landed in track {idx}')
            print(f'It will stay until time {self.tracks[idx]}')
        
    def departure_plane(self):
        idx = self.tracks.index(min(self.tracks))
        self.tracks[idx] = math.inf
        if self.verbose:
            print(f'Plain take off of track {idx}')
        if self.cnt_q > 0:
            self.insert_plane(idx)
            self.cnt_q -=1

    def calculate_time_in_airport(self):
        if self.verbose:
            print("Calculating total time in track")
        total_time = 0
        #Landing Time
        total_time+= rand.normal(10,5)
        if self.verbose:
            print(f'Landing time: {total_time}')
        #Fueling Time
        aditional_time = rand.exp(1/30)
        if self.verbose:
            print(f'Fueling time: {aditional_time}')
        total_time += aditional_time
        if rand.uniform() > 1/2:
            #Unloading Time
            aditional_time = rand.exp(1/30)
            if self.verbose:
                print(f'Unloading time: {aditional_time}')
            total_time += aditional_time
        if rand.uniform() > 1/2:
            #Loading Time
            aditional_time = rand.exp(1/30)
            if self.verbose:
                print(f'Loading time: {aditional_time}')
            total_time += aditional_time
        if rand.uniform() <= 0.1:
            #Repair Time
            aditional_time = rand.exp(1/15)
            if self.verbose:
                print(f'Repair time: {aditional_time}')
            total_time += aditional_time
        #Takeoff Time
        aditional_time = rand.normal(10,5)
        if self.verbose:
                print(f'Takeoff time: {aditional_time}')
        total_time += aditional_time
        return total_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simulates 5 tracks of a Airport and return\
        total empty time for each track')
    parser.add_argument('--max_time', metavar='T', type=int,\
        help='Max time of the simulation (in  minutes), default set to 10080')
    parser.add_argument('--verbose', metavar='V', type = bool,\
        help='Make the simulation verbose', default=False,  action=argparse.BooleanOptionalAction)
    
    T = 7 * 24 * 60
    verbose = False    
    args = parser.parse_args()
  
    if args.max_time:
        T = args.max_time
    if args.verbose:
        verbose = args.verbose 
    Airport(T, verbose).run()