from person import *
import argparse
# from torch.utils.tensorboard import SummaryWriter
import matplotlib.pyplot as plt
import utils.plotter
from utils.history_logger import HistoryLogger
history_logger = HistoryLogger()

# writer = SummaryWriter()
plotter = utils.plotter.Plotter()
Logger.set_level(Logger.IMPORTANT)


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
        people.append(person)
        Logger.info(person.get_description(detail_level="full"))
        history_logger.init_history(person)

    Logger.important(f"{args.start_pop} people created")

    ### Simulation Loop ###
    for step in range(args.sim_loop):
        Logger.print_title(f"Begining of loop {step}", char='=', length=10)
        num_match = 0

        # increase age and check for natural death
        Logger.print_title(f"Natural Death")
        for person in people:
            dead = person.grow_old()
            if dead:
                history_logger.log_death(person, "Natural Death")
        # filter out the dead
        people = list(filter(lambda p: p.alive, people))

        # socialize with ppl, and rank them
        Logger.print_title(f"Socialize")
        for person in people:
            Logger.info(Logger.divider())
            num_social, num_acquaint = person.socialize(people)
            history_logger.log_socialize_history(person, num_social)

            # add data to plots
            plotter.add_scatter("social level vs num social", person.mental_attrs.social_level,
                                num_social, xlabel="social_level", ylabel="num_social")
            plotter.add_scatter("social level vs num acquaint", person.mental_attrs.social_level,
                                num_acquaint, xlabel="social_level", ylabel="num_acquaint")

        for person in people:
            person.rank_acquaintances(people)
            history_logger.log_partner_target(person)

        # find match base on scores
        Logger.print_title(f"Finding Matches")
        for person in people:
            Logger.info(Logger.divider())
            found_match, match_result = person.find_match()
            if found_match:
                num_match += 1
            history_logger.log_match_result(person, match_result)

        for person in people:
            person.post_social()

        # Population wide stats
        plotter.add_scalar('Population', y=len(people), x=step,
                           xlabel='steps', ylabel='population')
        plotter.add_scalar('Match found', y=num_match, x=step,
                           xlabel='steps', ylabel='matchs found')

        Logger.print_title("Stats")
        Logger.important(
            f"Total match found is {Logger.blue(num_match)} ({num_match//2} pairs)")
        Logger.important(f"Population size is {Logger.blue(len(people))}")
        # end of step

    # DONE: make the plt somewhere else
    plotter.plot()
    Logger.print_title("End of simulation", char='=', length=10)

    history_logger.print_history(people[0].id)


if __name__ == '__main__':
    main()


'''
python ./src/simulate.py \
    --start_pop=100 \
    --sim_loop=1
'''
