from person import *
import argparse
# from torch.utils.tensorboard import SummaryWriter
import matplotlib.pyplot as plt
import utils.plotter

# writer = SummaryWriter()
plotter = utils.plotter.Plotter()


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
    nums_social = []
    nums_acquant = []
    social_levels = []

    for step in range(args.sim_loop):
        print(f"***** Begining of loop {step} *****")
        for person in people:
            # increase age and check for natural death
            person.grow_old()

            # attempt to find mate
            num_social, num_acquaint = person.socialize(people)

            plotter.add_scatter("social level vs num social", person.mental_attrs.social_level,
                                num_social, xlabel="social_level", ylabel="num_social")
            plotter.add_scatter("social level vs num acquaint", person.mental_attrs.social_level,
                                num_acquaint, xlabel="social_level", ylabel="num_acquaint")

        # at last, filter out the dead
        people = list(filter(lambda p: p.alive, people))
        plotter.add_scalar('Population', y=len(people), x=step,
                           xlabel='steps', ylabel='population')
        print(f"Population size is {len(people)}")

        # DONE: make the plt somewhere else
        plotter.plot()


if __name__ == '__main__':
    main()


'''
python ./src/simulate.py \
    --start_pop=100 \
    --sim_loop=1
'''
