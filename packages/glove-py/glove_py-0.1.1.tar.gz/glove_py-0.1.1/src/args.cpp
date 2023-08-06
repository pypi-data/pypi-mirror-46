#include "args.h"

void Args::parseArgs(const std::vector<std::string> &args) {
    std::string command(args[1]);
    for (int ai = 1; ai < args.size(); ai += 2) {
//        cout<<"args.at(ai + 1):"<<args.at(ai + 1)<<endl;
        if (args[ai][0] != '-') {
            std::cerr << "Provided argument without a dash! Usage:" << std::endl;
            printHelp();
            exit(EXIT_FAILURE);
        }
        try {
            if (args[ai] == "-h") {
                std::cerr << "Here is the help! Usage:" << std::endl;
                printHelp();
                exit(EXIT_FAILURE);
            } else if (args[ai] == "-vocab_size") { vocab_size = std::stoi(args.at(ai + 1)); }
            else if (args[ai] == "-min_count") { min_count = std::stoi(args.at(ai + 1)); }
            else if (args[ai] == "-window") { window = std::stoi(args.at(ai + 1)); }
            else if (args[ai] == "-embed_size") { embed_size = std::stoi(args.at(ai + 1)); }
            else if (args[ai] == "-max_size") { max_size = std::stoi(args.at(ai + 1)); }
            else if (args[ai] == "-epoch") { epoch = std::stoi(args.at(ai + 1)); }
            else if (args[ai] == "-threads") { threads = std::stoi(args.at(ai + 1)); }
            else if (args[ai] == "-threshold") { threshold = std::stoi(args.at(ai + 1)); }
            else if (args[ai] == "-seed") { seed = std::stoi(args.at(ai + 1)); }
            else if (args[ai] == "-lr") { lr = atof(args.at(ai + 1).c_str()); }


            else if (args[ai] == "-inputFile") { inputFile = args.at(ai + 1).c_str(); }
            else if (args[ai] == "-logdir") { logdir = args.at(ai + 1).c_str(); }
            else {
                std::cerr << "Unknown argument: " << args[ai] << std::endl;
                printHelp();
                exit(EXIT_FAILURE);
            }
        }
        catch (std::out_of_range) {
            std::cerr << args[ai] << " is missing an argument" << std::endl;
            printHelp();
            exit(EXIT_FAILURE);
        }
    }
}

void Args::printHelp() {
    cout << "this is help info" << endl
         << "this is help info......" << endl;
}



