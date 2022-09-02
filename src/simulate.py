from ast import While
from person import *
import argparse
# from torch.utils.tensorboard import SummaryWriter
import matplotlib.pyplot as plt
import utils.plotter
from utils.history_logger import HistoryLogger
from utils.command_parser import CommandParser

history_logger = HistoryLogger()

plotter = utils.plotter.Plotter()
Logger.set_level(Logger.IMPORTANT)


def simulation_step(step, people):
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
        kwargs = {'s': 4, 'alpha': 0.2}
        plotter.add_scatter("num social vs social level", person.mental_attrs.social_level,
                            num_social, xlabel="social_level", ylabel="num_social", kwargs=kwargs)
        plotter.add_scatter("num acquaint vs social level", person.mental_attrs.social_level,
                            num_acquaint, xlabel="social_level", ylabel="num_acquaint", kwargs=kwargs)
        plotter.add_scatter("num acquaint vs num social", x=num_social,
                            y=num_acquaint, xlabel="num_social", ylabel="num_acquaint", kwargs=kwargs)

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
    # NOTE: end of step


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
        simulation_step(step, people)

    ### log end of simulation stats ###
    kwargs = {'s': 4, 'alpha': 0.6}
    for pid, history in history_logger.history_dict.items():
        plotter.add_scatter('match made vs social level', y=history.get_success_match_num(), x=history.person.mental_attrs.social_level,
                            xlabel='social level', ylabel='match made', kwargs=kwargs)
        plotter.add_scatter('match made vs attractiveness', y=history.get_success_match_num(), x=history.person.physical_attrs.attractiveness,
                            xlabel='attractiveness', ylabel='match made', kwargs=kwargs)
        plotter.add_scatter('match made vs age', y=history.get_success_match_num(), x=history.person.basic_attrs.get_age_in_years(),
                            xlabel='age', ylabel='match made', kwargs=kwargs)
        plotter.add_scatter('match made vs height', y=history.get_success_match_num(), x=history.person.physical_attrs.height,
                            xlabel='height', ylabel='match made', kwargs=kwargs)

    # DONE: make the plt somewhere else
    plotter.plot()

    Logger.print_title("End of simulation", char='=', length=10)

    ### Command ###
    command_parser = CommandParser.get_default_parser(people, history_logger)
    Logger.print_title("CMD LINE ENV", char='-', total_length=80,
                       divider=Logger.divider(char='-', length=80))
    while True:
        command_txt = input(f"{Logger.bold(Logger.green('$ Command'))}: ")
        command_parser.parse_command(command_txt)


if __name__ == '__main__':
    main()


'''
python ./src/simulate.py \
    --start_pop=100 \
    --sim_loop=1
'''
