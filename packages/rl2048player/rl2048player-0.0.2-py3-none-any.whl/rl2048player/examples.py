import matplotlib.pyplot as plt
from .agents import QAgent, TD0Agent, SARSAAgent
from .masks import Mask_rxcx4


def example1(q_gif_file='example_output/example1/QGame.gif',
             td0_gif_file='example_output/example1/TD0Game.gif',
             sarsa_gif_file='example_output/example1/SARSAGAme.gif',
             graph_file='example_output/example1/graph.png'):
    mask = Mask_rxcx4()
    qagent = QAgent(mask)
    td0agent = TD0Agent(mask)
    sarsaagent = SARSAAgent(mask)
    qscores = qagent.train(6000)
    td0scores = td0agent.train(6000)
    sarsacores = sarsaagent.train(6000)
    qagent.makeGif(q_gif_file, graphic_size=200, top_margin=20,
                   seperator_width=6, num_trials=50)
    td0agent.makeGif(td0_gif_file, graphic_size=200, top_margin=20,
                     seperator_width=6, num_trials=50)
    sarsaagent.makeGif(sarsa_gif_file, graphic_size=200, top_margin=20,
                       seperator_width=6, num_trials=50)
    qagent.makeGraph(scores=qscores, rollingWindow=200)
    td0agent.makeGraph(scores=td0scores, rollingWindow=200)
    sarsaagent.makeGraph(scores=sarsacores, rollingWindow=200)
    plt.legend()
    plt.savefig(graph_file)


def example2(save_file='example_output/example2/agent.pickle',
             log_file='example_output/example2/log.csv',
             graph1_file='example_output/example2/graph1.png',
             graph2_file='example_output/example2/graph2.png'):
    mask = Mask_rxcx4()
    agent = TD0Agent(mask)
    scores = agent.train(2500, log_file)
    agent.makeGraph(scores=scores, graphFile=graph1_file, rollingWindow=100)
    agent.save(save_file)
    agent.load(save_file)
    agent.train(2500, log_file, 'a')
    agent.makeGraph(logFile=log_file, graphFile=graph2_file, rollingWindow=100)
    agent.save(save_file)
