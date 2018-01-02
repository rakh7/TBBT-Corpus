import json
import requests
from lxml import html

class conversation:
    def __init__(self, speaker, words):
        self.speaker = speaker
        self.addresse = []
        self.topic = None
        self.words = words

    def addAddresse(self, p_list):
        self.addresse = p_list

    def __str__(self):
        info_string = {}
        info_string["Speaker"] = self.speaker
        info_string["addresse"] = self.addresse
        info_string["words"] = self.words
        return str(info_string)

class Scene:
    def __init__(self, scene_desc= None, episode = None):
        self.episode = episode
        self.scene_desc = scene_desc
        self.conversation_list = []
        self.participants = []

    def addConversation(self, conv):
        self.conversation_list.append(conv)

    def addParticipants(self, actors):
        self.participants = list(actors)

    def __str__(self):
        info_str = self.scene_desc 
        for c in self.conversation_list:
            info_str += str(c)
        return str(info_str)

class getEpisodeTranscripts:
    def __init__(self):
        self.episodeInfo = {}
        self.Info = []
        self.allTranscripts = {}

    """
        Load the file that contains links for all episode and season
    """
    def loadEpisodeLinks(self, filename):
        with open(filename,"r") as fhandle:
            self.episodeInfo =  json.load(fhandle)
            fhandle.close()

    """
        Using lxml and requests to read content of the web page and
        capture the transcripts from the URL
    """
    def getEpisodeText(self, season, index):
        if season not in self.episodeInfo:
            raise Exception("Not a valid season for TBBT")
        ep, title, link = self.episodeInfo[season][index]
        try:
            page = requests.get(link)
            tree = html.fromstring(page.content)
            p_count = tree.find_class('entrytext')[0]
        except:
            raise Exception("Failed for {ep}, {season}".format(ep=ep,season=season))    
        return p_count.text_content(),ep

    """
        Map each cnonversation to a logical form
    """
    def processText(self, transcript, season, episode):
        scenes = transcript.split("Scene:")
        for s in scenes:
            tt = s.split("\n")
            scene_desc = tt[0]
            info = season+"_"+str(episode)
            sc = Scene(scene_desc,info)
            actors = []
            for t in tt[1:]:
                try:
                    (speaker, dialogue) =  t.split(":")
                    words = dialogue.split(" ")
                    conv = conversation(speaker,words)
                    actors.append(speaker)
                    sc.addConversation(conv)
                except ValueError:
                    pass
            actors = set(actors) # get only the unique ones
            sc.addParticipants(actors)
            for c in sc.conversation_list:
                # all people in the scene except the speaker are treated recipients
                c.addresse = list(filter(lambda x:  x != c.speaker,actors))
            self.Info.append(sc)


    def inspectValues(self):
        """
            Get the content in plain text format. Can deserialize the object to get info
            in JSON format. That's a TODO
        """
        info = []
        for scene in self.Info:
            sc = {}
            sc["Scene"] = scene.scene_desc
            sc["Partcipiants"] = scene.participants
            sc["Turns"] = []
            for c in scene.conversation_list:
                turn = {}
                turn["Speaker"] = c.speaker
                turn["Words"] = c.words
                turn["Recipients"] = c.addresse
                sc["Turns"].append(turn)
            info.append(sc)
        with open("final.json","w") as fh:
            json.dump(info,fh,indent=4)
            fh.close()

    def readTranscripts(self):
        """
            Use the file that has episode and transcript mapping to process
            each scene in the episode and capture all conversations
        """
        with open("all_info.json","r") as fhandle:
            Transcripts = json.load(fhandle)
            fhandle.close()
        for k in Transcripts:
            (episode,season) = k.split("_")
            self.processText(Transcripts[k],season, episode)
        self.inspectValues()

    def getAll(self):
        """
            Use this function to read all URLS and generate a transcripts
            in a JSON format where key is Episode_Season
        """
        self.loadEpisodeLinks("temp.json")
        try:
            for season in self.episodeInfo:
                #Season is the key
                for idx in range(0,len(self.episodeInfo[season])):
                    transcript,episode = self.getEpisodeText(season,idx)
                    ep_id = season+"_"+str(episode)
                    self.allTranscripts[ep_id] = transcript
                    #self.processText(transcript,season,episode)
        except:
            print("Error for somethings")
            with open("all_info.json","w") as fhandle:
                json.dump(self.allTranscripts,fhandle)
                fhandle.close()
        with open("all_info.json","w") as fhandle:
                json.dump(self.allTranscripts,fhandle)
                fhandle.close()

t = getEpisodeTranscripts()
t.readTranscripts()