from optparse import OptionParser


def checkThresh(l) :
    if len(l) != 2 :
        return False
    if int(l[0]) >= int(l[1]) :
        return False
    return True
    


def cGen(filename, col) :
    if filename == None :
        return f'{col} = _;\n\n'
    else :
        irng = input(f"* {col} instrument frequency range: ").split("-")
        frng = irng if checkThresh(irng) else ["100", "400"]
        thresh.write(f'{col}={int(frng[0])}-{int(frng[1])}\n')
        # gain = f'hslider("{col}Gain[osc:/main/{col}Gain]",0,0,1,0.01)'
        # freq = f'hslider("{col}Freq[osc:/main/{col}Freq]",{frng[0]},{frng[0]},{frng[1]},1)'
        freq = f'{col}f = hslider("{col}Freq",{frng[0]},{frng[0]},{frng[1]},1) : si.smoo;\n'
        gain = f'{col}g = hslider("{col}Gain",0,0,1,0.01) : si.smoo;\n'
        comp = f'{col} = component("{filename}")({col}f, {col}g);\n\n'
        return f'{freq}{gain}{comp}'

def fGen(options) :
    imp = 'import("stdfaust.lib");\n'
    osc = 'declare options "[osc:on]";\n\n'
    red = cGen(options.reddsp, "red")
    ylo = cGen(options.yellowdsp, "yellow") 
    blu = cGen(options.bluedsp, "blue") 
    grn = cGen(options.greendsp, "green")
    end = 'process = red, yellow, blue, green :> _ <: _, _;\n'
    return f'{imp}{osc}{red}{ylo}{blu}{grn}{end}'


if __name__ == "__main__":

    thresh = open("thresh.txt", "w")

    parser = OptionParser()

    parser.add_option("--red", "-r", dest="reddsp",
                    help="Red Object Synth", metavar="FILE")
    parser.add_option("--green", "-g", dest="greendsp",
                    help="Green Object Synth", metavar="FILE")
    parser.add_option("--blue", "-b", dest="bluedsp",
                    help="Blue Object Synth", metavar="FILE")
    parser.add_option("--yellow", "-y", dest="yellowdsp",
                    help="Yellow Object Synth", metavar="FILE")
                    
    (options, args) = parser.parse_args()

    file = open("main.dsp", "w")
    file.write(fGen(options))
    file.close
    thresh.close





# file = open("test.dsp", "r")
# f2 = open("t.dsp", "w")
# f2.write(file.read())

# def genFaust 

# # do I need to parse component files for import statements?


#     print(f"Arguments count: {len(sys.argv)}")
#     for i, arg in enumerate(sys.argv):
#         print(f"Argument {i:>6}: {arg}")




# count = 0
    # for u in [red, ylo, blu, grn] :
    #     print(u[-3])
    #     if u[-3] == "_" :
    #         count += 1
    # op = ":>" if count > 1 else "<:"