from person import *
import argparse
from torch.utils.tensorboard import SummaryWriter
import matplotlib.pyplot as plt

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
    people: List[Person] = []
    for _ in range(args.start_pop):
        person = Person.generate_random_person(age_bounds=(20*12, 50*12))
        print(person.get_description(detail_level="full"))
        people.append(person)

    print(f"{args.start_pop} people created")

    ### Simulation Loop ###
    nums = []
    socials = []
    for step in range(args.sim_loop):
        print(f"***** Begining of loop {step} *****")
        for person in people:
            # increase age and check for natural death
            person.grow_old()

            # attempt to find mate
            num_social = person.socialize(people)

            nums.append(num_social)
            socials.append(person.mental_attrs.social_level)

        # at last, filter out the dead
        people = list(filter(lambda p: p.alive, people))
        writer.add_scalar('Population', len(people), step)
        print(f"Population size is {len(people)}")

        # TODO: make the plt somewhere else
        fig = plt.figure()
        plt.scatter(nums, socials)
        writer.add_figure("matplot", fig)
        writer.flush()


if __name__ == '__main__':
    main()


'''
python ./simulate.py \
    --start_pop=200 \
    --sim_loop=1
'''
