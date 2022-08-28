from person import *
import argparse
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter()

def main():
    ### Parse Arguments ###
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_pop", type=int, required=True)
    parser.add_argument("--sim_loop", type=int, required=True)

    args, _ = parser.parse_known_args()
    print(args)

    ### Start of Dawn ###
    # create starting population
    people = []
    for _ in range(args.start_pop):
        person = Person.generate_random_person()
        print(person.get_description())
        people.append(person)

    print(f"{args.start_pop} people created")

    ### Simulation Loop ###
    for step in range(args.sim_loop):
        print(f"***** Begining of loop {step} *****")
        for person in people:
            # increase age and check for natural death
            person.grow_old() 

            # attempt to find mate
            person.socialize()

        # at last, filter out the dead
        people = list(filter(lambda p: p.alive, people))
        writer.add_scalar('Population',len(people), step)
        print(f"Population size is {len(people)}")
            


if __name__ == '__main__':
    main()


'''
python ./Population_Simulation/simulate.py \
    --start_pop=100 \
    --sim_loop=100
'''
