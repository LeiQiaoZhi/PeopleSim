from person import *
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_pop", type=int, required=True)
    parser.add_argument("--sim_loop", type=int, required=True)

    args, _ = parser.parse_known_args()
    print(args)

    ### Start of Dawn ###
    # create starting population
    people = []
    for _ in range(args.start_pop):
        person = Person(BasicAttributes.get_random_basic_attributes())
        print(person.get_basic_description())
        people.append(person)

    print(f"{args.start_pop} people created")

    # Simulation Loop
    for loop in range(args.sim_loop):
        print(f"***** Begining of loop {loop} *****")
        for person in people:
            person.grow_old()


if __name__ == '__main__':
    main()


'''
python ./Population_Simulation/simulate.py \
    --start_pop=10 \
    --sim_loop=100
'''
