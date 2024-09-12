from bone_handler import getBoneTree, drawNewBones
from class_def import *
import os


#model_filename = "Alien Jippo Jim.bin"
#anim_filename = "testing_bins/010da8.bin"


transformation_type_index = {
    0: "X Rot",
    1: "Y Rot",
    2: "Z Rot",
    3: "X Scale",
    4: "Y Scale",
    5: "Z Scale",
    6: "X Trans",
    7: "Y Trans",
    8: "Z Trans"
}


def checkHeader(filename):
    with open(filename, "rb") as file:
        startFrame = int.from_bytes(file.read(2), "big")
        endFrame = int.from_bytes(file.read(2), "big")
        elementCount = int.from_bytes(file.read(2), "big")
        file.seek(2, 1)
        return startFrame, endFrame, elementCount

def get_animation(anim_filename):
    startFrame, endFrame, elementCount = checkHeader(anim_filename)
    animation = Animation(startFrame, endFrame, elementCount)
    string = "Start Frame: {}\nEnd Frame: {}\nElement Count: {}".format(startFrame, endFrame, elementCount)
    with open(anim_filename, "rb") as file:
        file.seek(8)
        for element in range(elementCount):
            elementInfo = int.from_bytes(file.read(2), "big")
            bone_id = (elementInfo & 0xFFF0) >> 4
            transformation_type = transformation_type_index[elementInfo & 0xF]
            dataCount = int.from_bytes(file.read(2), "big")
            string += "\n\nElement {} | Bone {} | Type: {} | Data Count {}".format(element, hex(bone_id), transformation_type, dataCount)
            animation.elements.append(Element(bone_id, transformation_type, dataCount))
            for data in range(dataCount):
                elementData = int.from_bytes(file.read(2), "big")
                unknown = (elementData & 0xC000) >> 14
                frame = elementData & 0x3FFF
                transform_factor = int.from_bytes(file.read(2), "big", signed=True) / 64
                string += "\n\tData {} | Unk {} | Frame {} | Factor = {}".format(data, unknown, frame, transform_factor)
                animation.elements[element].data.append(Data(unknown, frame, transform_factor))
    output = input("Output file name: ")
    with open(output, "w") as file:
        file.write(string)

load_model = input("Load Model? (y)/n\n")
if load_model != "n":
    model_filename = input("Model File: ")
    bones = getBoneTree(model_filename)
    drawNewBones(bones)
load_animation = input("Load Animation? (y)/n\n")
if load_animation != "n":
    anim_filename = input("Animation File: ")
    get_animation(anim_filename)