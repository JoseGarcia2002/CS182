english_word_list = open("english_words_list.txt",'r').readlines()
english_word_list = [word.rstrip("\n") for word in english_word_list]

class CaesarCipher:
    def __init__(self, alphabet=None, cipherkey=None):
        #### YOUR CODE HERE ####
        if alphabet is None:
            alphabet =list('abcdefghijklmnopqrstuvwxyz')

        self.alphabet = alphabet
        self.cipherkey = cipherkey

    def encrypt(self, plaintext:str, cipherkey:str = None)->str:
        """Convert plaintext to ciphertext using a cipherkey"""
        #### YOUR CODE HERE ####
        if cipherkey is not None:
            self.cipherkey = cipherkey
        
        if self.cipherkey not in self.alphabet:
            raise AttributeError

        ciphertext = ''
        offset = self.alphabet.index(self.cipherkey)
        modulus = len(self.alphabet)

        for char in plaintext:
            try:
                ciphertext += self.alphabet[(offset + self.alphabet.index(char)) % modulus]
            except ValueError:
                ciphertext += char
        return ciphertext

    
    def decrypt(self, ciphertext:str, cipherkey:str = None)->str:
        """Convert ciphertext to plaintext using a cipherkey"""
        #### YOUR CODE HERE ####
        if cipherkey is not None:
            self.cipherkey = cipherkey
        
        if self.cipherkey not in self.alphabet:
            raise AttributeError

        plaintext = ''
        offset = self.alphabet.index(self.cipherkey)
        modulus = len(self.alphabet)

        for char in ciphertext:
            try:
                plaintext += self.alphabet[(-offset + self.alphabet.index(char)) % modulus]
            except ValueError:
                plaintext += char
        return plaintext
    
    def auto_decrypt(self, ciphertext:str, english_word_list:list, verbose=False)->tuple:
        """Decrypt a ciphertext by iteratively searching for the most likely cipherkey"""
        #### YOUR CODE HERE ####
        frequencies = {}
        plaintexts = {}

        for potentialKey in self.alphabet:
            plaintext = self.decrypt(ciphertext, potentialKey)
            plaintexts[potentialKey] = plaintext

            punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            plaintextNoPunc = ''

            wordsCounted = 0
            wordsSat = 0

            for char in plaintext:
                if char not in punctuation:
                    plaintextNoPunc += char.lower()
            
            words = plaintextNoPunc.split(" ")

            for word in words:
                wordsCounted += 1
                if word in english_word_list:
                    wordsSat += 1
            
            frequencies[potentialKey] = wordsSat/wordsCounted

            if verbose:
                print(potentialKey, frequencies[potentialKey])

            if frequencies[potentialKey] > 0.85:
                return (plaintext, potentialKey)

        bestKey = max(frequencies, key=frequencies.get)
        return (plaintexts[bestKey], bestKey)

    def auto_decrypt_bonus(self, ciphertext:str, english_word_list:list, verbose=False)->tuple:
        """Bonus Problem: A faster, more efficient method of auto-decrypting a Caesar Cipher"""
        text_freq = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}

        first_letter = ''
        for char in ciphertext:
            if ((char in self.alphabet) and (first_letter == '')):
                first_letter = char
                break

        for char in ciphertext:
            if char in self.alphabet: 
                text_freq[char.lower()] += 1

        #print(text_freq)
        #print(dict(sorted(text_freq.items(), key=lambda item: item[1])))
        frequencies = {}
        plaintexts = {}

        for i in range(26):
            max_key = max(text_freq, key=text_freq.get)
            offset = (self.alphabet.index(max_key) - 4) % 52
            potential_key = self.alphabet[offset]
            
            plaintext = self.decrypt(ciphertext, potential_key)

            plaintexts[potential_key] = plaintext

            punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            plaintextNoPunc = ''

            wordsCounted = 0
            wordsSat = 0

            for char in plaintext:
                if char not in punctuation:
                    plaintextNoPunc += char.lower()
            
            words = plaintextNoPunc.split(" ")

            for word in words:
                wordsCounted += 1
                if word in english_word_list:
                    wordsSat += 1
            
            frequencies[potential_key] = wordsSat/wordsCounted

            if verbose:
                print(potential_key, frequencies[potential_key])

            if frequencies[potential_key] > 0.50:
                #print(plaintext)
                #print(potential_key)
                return (plaintext, potential_key)
            text_freq[max_key] = 0

        bestKey = max(frequencies, key=frequencies.get)
        return (plaintexts[bestKey], bestKey)

alph = "abcdefghijklmnopqrstuvwxyz"
full_alph = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
test_cipher = CaesarCipher(alphabet=full_alph)

plaintext = "The next point is the color of the mature caterpillars, some of which are brown. This probably makes the caterpillar even more conspicuous among the green leaves than would otherwise be the case. Let us see, then, whether the habits of the insect will throw any light upon the riddle. What would you do if you were a big caterpillar? Why, like most other defenseless creatures, you would feed by night, and lie concealed by day. So do these caterpillars. When the morning light comes, they creep down the stem of the food plant, and lie concealed among the thick herbage and dry sticks and leaves, near the ground, and it is obvious that under such circumstances the brown color really becomes a protection. It might indeed be argued that the caterpillars, having become brown, concealed themselves on the ground, and that we were reversing the state of things. But this is not so, because, while we may say as a general rule that large caterpillars feed by night and lie concealed by day, it is by no means always the case that they are brown; some of them still retaining the green color. We may then conclude that the habit of concealing themselves by day came first, and that the brown color is a later adaptation."
ciphertext = "aol ulEA wvpuA pz Aol jvsvy vm Aol thAByl jhAlywpsshyz, zvtl vm Dopjo hyl iyvDu. aopz wyvihisF thrlz Aol jhAlywpsshy lClu tvyl jvuzwpjBvBz htvun Aol nyllu slhClz Aohu DvBsk vAolyDpzl il Aol jhzl. SlA Bz zll, Aolu, DolAoly Aol ohipAz vm Aol puzljA Dpss AoyvD huF spnoA Bwvu Aol ypkksl. dohA DvBsk FvB kv pm FvB Dlyl h ipn jhAlywpsshy? doF, sprl tvzA vAoly klmluzlslzz jylhABylz, FvB DvBsk mllk iF upnoA, huk spl jvujlhslk iF khF. Zv kv Aolzl jhAlywpsshyz. dolu Aol tvyupun spnoA jvtlz, AolF jyllw kvDu Aol zAlt vm Aol mvvk wshuA, huk spl jvujlhslk htvun Aol Aopjr olyihnl huk kyF zApjrz huk slhClz, ulhy Aol nyvBuk, huk pA pz viCpvBz AohA Bukly zBjo jpyjBtzAhujlz Aol iyvDu jvsvy ylhssF iljvtlz h wyvAljApvu. PA tpnoA pukllk il hynBlk AohA Aol jhAlywpsshyz, ohCpun iljvtl iyvDu, jvujlhslk AoltzlsClz vu Aol nyvBuk, huk AohA Dl Dlyl ylClyzpun Aol zAhAl vm Aopunz. IBA Aopz pz uvA zv, iljhBzl, Dopsl Dl thF zhF hz h nlulyhs yBsl AohA shynl jhAlywpsshyz mllk iF upnoA huk spl jvujlhslk iF khF, pA pz iF uv tlhuz hsDhFz Aol jhzl AohA AolF hyl iyvDu; zvtl vm Aolt zApss ylAhpupun Aol nyllu jvsvy. dl thF Aolu jvujsBkl AohA Aol ohipA vm jvujlhspun AoltzlsClz iF khF jhtl mpyzA, huk AohA Aol iyvDu jvsvy pz h shAly hkhwAhApvu."

#plaintext = "the next point is the color of the mature caterpillars, some of which are brown. this probably makes the caterpillar even more conspicuous among the green leaves than would otherwise be the case. let us see, then, whether the habits of the insect will throw any light upon the riddle. what would you do if you were a big caterpillar? why, like most other defenseless creatures, you would feed by night, and lie concealed by day. so do these caterpillars. when the morning light comes, they creep down the stem of the food plant, and lie concealed among the thick herbage and dry sticks and leaves, near the ground, and it is obvious that under such circumstances the brown color really becomes a protection. it might indeed be argued that the caterpillars, having become brown, concealed themselves on the ground, and that we were reversing the state of things. but this is not so, because, while we may say as a general rule that large caterpillars feed by night and lie concealed by day, it is by no means always the case that they are brown; some of them still retaining the green color. we may then conclude that the habit of concealing themselves by day came first, and that the brown color is a later adaptation."
#ciphertext = "aol ulea wvpua pz aol jvsvy vm aol thabyl jhalywpsshyz, zvtl vm dopjo hyl iyvdu. aopz wyvihisf thrlz aol jhalywpsshy lclu tvyl jvuzwpjbvbz htvun aol nyllu slhclz aohu dvbsk vaolydpzl il aol jhzl. sla bz zll, aolu, dolaoly aol ohipaz vm aol puzlja dpss aoyvd huf spnoa bwvu aol ypkksl. doha dvbsk fvb kv pm fvb dlyl h ipn jhalywpsshy? dof, sprl tvza vaoly klmluzlslzz jylhabylz, fvb dvbsk mllk if upnoa, huk spl jvujlhslk if khf. zv kv aolzl jhalywpsshyz. dolu aol tvyupun spnoa jvtlz, aolf jyllw kvdu aol zalt vm aol mvvk wshua, huk spl jvujlhslk htvun aol aopjr olyihnl huk kyf zapjrz huk slhclz, ulhy aol nyvbuk, huk pa pz vicpvbz aoha bukly zbjo jpyjbtzahujlz aol iyvdu jvsvy ylhssf iljvtlz h wyvaljapvu. pa tpnoa pukllk il hynblk aoha aol jhalywpsshyz, ohcpun iljvtl iyvdu, jvujlhslk aoltzlsclz vu aol nyvbuk, huk aoha dl dlyl ylclyzpun aol zahal vm aopunz. iba aopz pz uva zv, iljhbzl, dopsl dl thf zhf hz h nlulyhs ybsl aoha shynl jhalywpsshyz mllk if upnoa huk spl jvujlhslk if khf, pa pz if uv tlhuz hsdhfz aol jhzl aoha aolf hyl iyvdu; zvtl vm aolt zapss ylahpupun aol nyllu jvsvy. dl thf aolu jvujsbkl aoha aol ohipa vm jvujlhspun aoltzlsclz if khf jhtl mpyza, huk aoha aol iyvdu jvsvy pz h shaly hkhwahapvu."

long_plaintext = """ He slowly poured the drink over a large chunk of ice he has especially chiseled off a larger block. He didn  t particularly like his drinks cold, but he knew that the drama of chiseling the ice and then pouring a drink over it looked far more impressive than how he actually liked it. It was all about image and he  d managed to perfect the image that he wanted to project.
Here  s the thing. She doesn  t have anything to prove, but she is going to anyway. That  s just her character. She knows she doesn  t have to, but she still will just to show you that she can. Doubt her more and she  ll prove she can again. We all already know this and you will too.
It was a scrape that he hardly noticed. Sure, there was a bit of blood but it was minor compared to most of the other cuts and bruises he acquired on his adventures. There was no way he could know that the rock that produced the cut had alien genetic material on it that was now racing through his bloodstream. He felt perfectly normal and continued his adventure with no knowledge of what was about to happen to him.
The song came from the bathroom belting over the sound of the shower  s running water. It was the same way each day began since he could remember. It listened intently and concluded that the singing today was as terrible as it had ever been.
Rhonda prided herself on always taking the path less traveled. She  d decided to do this at an early age and had continued to do so throughout her entire life. It was a point of pride and she would explain to anyone who would listen that doing so was something that she  d made great efforts to always do. She  d never questioned this decision until her five-year-old niece asked her,  So, is this why your life has been so difficult?  and Rhonda didn  t have an answer for her.
She never liked cleaning the sink. It was beyond her comprehension how it got so dirty so quickly. It seemed that she was forced to clean it every other day. Even when she was extra careful to keep things clean and orderly, it still ended up looking like a mess in a couple of days. What she didn  t know was there was a tiny creature living in it that didn  t like things neat.
He wondered if he should disclose the truth to his friends. It would be a risky move. Yes, the truth would make things a lot easier if they all stayed on the same page, but the truth might fracture the group leaving everything in even more of a mess than it was not telling the truth. It was time to decide which way to go.
The desert wind blew the tumbleweed in front of the car. Alex swerved to avoid the tumbleweed, but he turned the wheel a bit too strong and the car left the road and skidded onto the dirt median. He instantly slammed on the brakes and the car stopped in a cloud of dirt. When the dust cloud had settled and he could see around him again, he realized that he  d somehow crossed over into an entirely new dimension.
He heard the song coming from a distance, lightly floating over the air to his ears. Although it was soft and calming, he was wary. It seemed a little too soft and a little too calming for everything that was going on. He wanted it to be nothing more than beautiful music coming from the innocent and pure joy of singing, but in the back of his mind, he knew it was likely some type of trap.
The alarm went off and Jake rose awake. Rising early had become a daily ritual, one that he could not fully explain. From the outside, it was a wonder that he was able to get up so early each morning for someone who had absolutely no plans to be productive during the entire day.
Pink ponies and purple giraffes roamed the field. Cotton candy grew from the ground as a chocolate river meandered off to the side. What looked like stones in the pasture were actually rock candy. Everything in her dream seemed to be perfect except for the fact that she had no mouth.
 It doesn  t take much to touch someone  s heart,  Daisy said with a smile on her face.  It  s often just the little things you do that can change a person  s day for the better.  Daisy truly believed this to be the way the world worked, but she didn  t understand that she was merely a robot that had been programmed to believe this.
Things aren  t going well at all with mom today. She is just a limp noodle and wants to sleep all the time. I sure hope that things get better soon.
She looked at her student wondering if she could ever get through.  You need to learn to think for yourself,  she wanted to tell him.  Your friends are holding you back and bringing you down.  But she didn  t because she knew his friends were all that he had and even if that meant a life of misery, he would never give them up.
It all started with a random letter. Several of those were joined forces to create a random word. The words decided to get together and form a random sentence. They decided not to stop there and it wasn  t long before a random paragraph had been cobbled together. The question was whether or not they could continue the momentum long enough to create a random short story.
He couldn  t move. His head throbbed and spun. He couldn  t decide if it was the flu or the drinking last night. It was probably a combination of both.
He hid under the covers hoping that nobody would notice him there. It really didn  t make much sense since it would be obvious to anyone who walked into the room there was someone hiding there, but he still held out hope. He heard footsteps coming down the hall and stop in front in front of the bedroom door. He heard the squeak of the door hinges and someone opened the bedroom door. He held his breath waiting for whoever was about to discover him, but they never did.
The blinking light caught her attention. She thought about it a bit and couldn  t remember ever noticing it before. That was strange since it was obvious the flashing light had been there for years. Now she wondered how she missed it for that amount of time and what other things in her small town she had failed to notice.
It wasn  t supposed to end that way. The plan had been meticulously thought out and practiced again and again. There was only one possible result once it had been implemented, but as they stood there the result wasn  t anything close to what it should have been. They all blankly looked at each wondering how this could have happened. In their minds, they all began to blame the other members of the group as to why they had failed.
She had been told time and time again that the most important steps were the first and the last. It was something that she carried within her in everything she did, but then he showed up and disrupted everything. He told her that she had it wrong. The first step wasn  t the most important. The last step wasn  t the most important. It was the next step that was the most important.
Many people say that life isn  t like a bed of roses. I beg to differ. I think that life is quite like a bed of roses. Just like life, a bed of roses looks pretty on the outside, but when you  re in it, you find that it is nothing but thorns and pain. I myself have been pricked quite badly.
There was little doubt that the bridge was unsafe. All one had to do was look at it to know that with certainty. Yet Bob didn  t see another option. He may have been able to work one out if he had a bit of time to think things through, but time was something he didn  t have. A choice needed to be made, and it needed to be made quickly.
Debbie put her hand into the hole, sliding her hand down as far as her arm could reach. She wiggled her fingers hoping to touch something, but all she felt was air. She shifted the weight of her body to try and reach an inch or two more down the hole. Her fingers still touched nothing but air.
Sleeping in his car was never the plan but sometimes things don  t work out as planned. This had been his life for the last three months and he was just beginning to get used to it. He didn  t actually enjoy it, but he had accepted it and come to terms with it. Or at least he thought he had. All that changed when he put the key into the ignition, turned it and the engine didn  t make a sound.
Twenty-five hours had passed since the incident. It seemed to be a lot longer than that. That twenty-five hours seemed more like a week in her mind. The fact that she still was having trouble comprehending exactly what took place wasn  t helping the matter. She thought if she could just get a little rest the entire incident might make a little more sense.
Eating raw fish didn  t sound like a good idea.  It  s a delicacy in Japan,  didn  t seem to make it any more appetizing. Raw fish is raw fish, delicacy or not.
She glanced up into the sky to watch the clouds taking shape. First, she saw a dog. Next, it was an elephant. Finally, she saw a giant umbrella and at that moment the rain began to pour.
He was after the truth. At least, that  s what he told himself. He believed it, but any rational person on the outside could see he was lying to himself. It was apparent he was really only after his own truth that he  d already decided and was after this truth because the facts didn  t line up with the truth he wanted. So he continued to tell everyone he was after the truth oblivious to the real truth sitting right in front of him.
According to the caption on the bronze marker placed by the Multnomah Chapter of the Daughters of the American Revolution on May 12, 1939, College Hall (is) the oldest building in continuous use for Educational purposes west of the Rocky Mountains. Here were educated men and women who have won recognition throughout the world in all the learned professions.
 So, what do you think?  he asked nervously. He wanted to know the answer, but at the same time, he didn  t. He  d put his heart and soul into the project and he wasn  t sure he  d be able to recover if they didn  t like what he produced. The silence from the others in the room seemed to last a lifetime even though it had only been a moment since he asked the question.  So, what do you think?  he asked again.
She sat down with her notebook in her hand, her mind wandering to faraway places. She paused and considered all that had happened. It hadn  t gone as expected. When the day began she thought it was going to be a bad one, but as she sat recalling the day  s events to write them down, she had to admit, it had been a rather marvelous day.
She  s asked the question so many times that she barely listened to the answers anymore. The answers were always the same. Well, not exactly the same, but the same in a general sense. A more accurate description was the answers never surprised her. So, she asked for the 10,000th time,  What  s your favorite animal?  But this time was different. When she heard the young boy  s answer, she wondered if she had heard him correctly.
He took a sip of the drink. He wasn  t sure whether he liked it or not, but at this moment it didn  t matter. She had made it especially for him so he would have forced it down even if he had absolutely hated it. That  s simply the way things worked. She made him a new-fangled drink each day and he took a sip of it and smiled, saying it was excellent.
As she sat watching the world go by, something caught her eye. It wasn  t so much its color or shape, but the way it was moving. She squinted to see if she could better understand what it was and where it was going, but it didn  t help. As she continued to stare into the distance, she didn  t understand why this uneasiness was building inside her body. She felt like she should get up and run. If only she could make out what it was. At that moment, she comprehended what it was and where it was heading, and she knew her life would never be the same.
The paper was blank. It shouldn  t have been. There should have been writing on the paper, at least a paragraph if not more. The fact that the writing wasn  t there was frustrating. Actually, it was even more than frustrating. It was downright distressing.
They rushed out the door, grabbing anything and everything they could think of they might need. There was no time to double-check to make sure they weren  t leaving something important behind. Everything was thrown into the car and they sped off. Thirty minutes later they were safe and that was when it dawned on them that they had forgotten the most important thing of all.
There were two things that were important to Tracey. The first was her dog. Anyone that had ever met Tracey knew how much she loved her dog. Most would say that she treated it as her child. The dog went everywhere with her and it had been her best friend for the past five years. The second thing that was important to Tracey, however, would be a lot more surprising to most people.
The red line moved across the page. With each millimeter it advanced forward, something changed in the room. The actual change taking place was difficult to perceive, but the change was real. The red line continued relentlessly across the page and the room would never be the same.
She put the pen to paper but she couldn  t bring herself to actually write anything. She just stared at the blank card and wondered what words she could write that would help in even a small way. She thought of a dozen ways to begin but none seemed to do justice to the situation. There were no words that could help and she knew it.
To the two friends, the treehouse was much more than a treehouse. It was a sanctuary away from the other kids where they could be themselves without being teased or bullied. It was their secret fortress hidden high in the branches of a huge oak that only they knew existed. At least that is what they thought. They were more than a little annoyed when their two younger sisters decided to turn the treehouse into a princess castle by painting the inside pink and putting glitter everywhere.
The amber droplet hung from the branch, reaching fullness and ready to drop. It waited. While many of the other droplets were satisfied to form as big as they could and release, this droplet had other plans. It wanted to be part of history. It wanted to be remembered long after all the other droplets had dissolved into history. So it waited for the perfect specimen to fly by to trap and capture that it hoped would eventually be discovered hundreds of years in the future.
The bridge spanning a 100-foot gully stood in front of him as the last obstacle blocking him from reaching his destination. While people may have called it a  bridge , the reality was it was nothing more than splintered wooden planks held together by rotting ropes. It was questionable whether it would hold the weight of a child, let alone the weight of a grown man. The problem was there was no other way across the gully, and this played into his calculations of whether or not it was worth the risk of trying to cross it.
It probably seemed trivial to most people, but it mattered to Tracey. She wasn  t sure why it mattered so much to her, but she understood deep within her being that it mattered to her. So for the 365th day in a row, Tracey sat down to eat pancakes for breakfast.
He walked down the steps from the train station in a bit of a hurry knowing the secrets in the briefcase must be secured as quickly as possible. Bounding down the steps, he heard something behind him and quickly turned in a panic. There was nobody there but a pair of old worn-out shoes were placed neatly on the steps he had just come down. Had he past them without seeing them? It didn  t seem possible. He was about to turn and be on his way when a deep chill filled his body.
Hopes and dreams were dashed that day. It should have been expected, but it still came as a shock. The warning signs had been ignored in favor of the possibility, however remote, that it could actually happen. That possibility had grown from hope to an undeniable belief it must be destiny. That was until it wasn  t and the hopes and dreams came crashing down.
Twenty-five years Dana had been waiting. She tried to be patient during that time but she hadn  t always managed to be as patient as she  d like. But today the opportunity had finally come. The thing she always imagined would make her the happiest person in the world was about to happen. She didn  t know why at this specific time she all of a sudden felt sick inside.
Love isn  t always a ray of sunshine. That  s what the older girls kept telling her when she said she had found the perfect man. She had thought this was simply bitter talk on their part since they had been unable to find true love like hers. But now she had to face the fact that they may have been right. Love may not always be a ray of sunshine. That is unless they were referring to how the sun can burn.
Debbie knew she was being selfish and unreasonable. She understood why the others in the room were angry and frustrated with her and the way she was acting. In her eyes, it didn  t really matter how they felt because she simply didn  t care.
Do you think you  re living an ordinary life? You are so mistaken it  s difficult to even explain. The mere fact that you exist makes you extraordinary. The odds of you existing are less than winning the lottery, but here you are. Are you going to let this extraordinary opportunity pass?
There were little things that she simply could not stand. The sound of someone tapping their nails on the table. A person chewing with their mouth open. Another human imposing themselves into her space. She couldn  t stand any of these things, but none of them compared to the number one thing she couldn  t stand which topped all of them combined. """

long_ciphertext = """ Ol zsvDsF wvBylk Aol kypur vCly h shynl joBur vm pjl ol ohz lzwljphssF jopzlslk vmm h shynly isvjr. Ol kpku  A whyApjBshysF sprl opz kypurz jvsk, iBA ol rulD AohA Aol kyhth vm jopzlspun Aol pjl huk Aolu wvBypun h kypur vCly pA svvrlk mhy tvyl ptwylzzpCl Aohu ovD ol hjABhssF sprlk pA. PA Dhz hss hivBA pthnl huk ol  k thuhnlk Av wlymljA Aol pthnl AohA ol DhuAlk Av wyvqljA.
Olyl  z Aol Aopun. Zol kvlzu  A ohCl huFAopun Av wyvCl, iBA zol pz nvpun Av huFDhF. aohA  z qBzA oly johyhjAly. Zol ruvDz zol kvlzu  A ohCl Av, iBA zol zApss Dpss qBzA Av zovD FvB AohA zol jhu. KvBiA oly tvyl huk zol  ss wyvCl zol jhu hnhpu. dl hss hsylhkF ruvD Aopz huk FvB Dpss Avv.
PA Dhz h zjyhwl AohA ol ohyksF uvApjlk. ZByl, Aolyl Dhz h ipA vm isvvk iBA pA Dhz tpuvy jvtwhylk Av tvzA vm Aol vAoly jBAz huk iyBpzlz ol hjxBpylk vu opz hkCluABylz. aolyl Dhz uv DhF ol jvBsk ruvD AohA Aol yvjr AohA wyvkBjlk Aol jBA ohk hsplu nlulApj thAlyphs vu pA AohA Dhz uvD yhjpun AoyvBno opz isvvkzAylht. Ol mlsA wlymljAsF uvyths huk jvuApuBlk opz hkCluAByl DpAo uv ruvDslknl vm DohA Dhz hivBA Av ohwwlu Av opt.
aol zvun jhtl myvt Aol ihAoyvvt ilsApun vCly Aol zvBuk vm Aol zovDly  z yBuupun DhAly. PA Dhz Aol zhtl DhF lhjo khF ilnhu zpujl ol jvBsk yltltily. PA spzAlulk puAluAsF huk jvujsBklk AohA Aol zpunpun AvkhF Dhz hz Alyypisl hz pA ohk lCly illu.
Yovukh wypklk olyzlsm vu hsDhFz Ahrpun Aol whAo slzz AyhClslk. Zol  k kljpklk Av kv Aopz hA hu lhysF hnl huk ohk jvuApuBlk Av kv zv AoyvBnovBA oly luApyl spml. PA Dhz h wvpuA vm wypkl huk zol DvBsk lEwshpu Av huFvul Dov DvBsk spzAlu AohA kvpun zv Dhz zvtlAopun AohA zol  k thkl nylhA lmmvyAz Av hsDhFz kv. Zol  k ulCly xBlzApvulk Aopz kljpzpvu BuAps oly mpCl-Flhy-vsk upljl hzrlk oly,  Zv, pz Aopz DoF FvBy spml ohz illu zv kpmmpjBsA?  huk Yovukh kpku  A ohCl hu huzDly mvy oly.
Zol ulCly sprlk jslhupun Aol zpur. PA Dhz ilFvuk oly jvtwyloluzpvu ovD pA nvA zv kpyAF zv xBpjrsF. PA zlltlk AohA zol Dhz mvyjlk Av jslhu pA lClyF vAoly khF. LClu Dolu zol Dhz lEAyh jhylmBs Av rllw Aopunz jslhu huk vyklysF, pA zApss luklk Bw svvrpun sprl h tlzz pu h jvBwsl vm khFz. dohA zol kpku  A ruvD Dhz Aolyl Dhz h ApuF jylhAByl spCpun pu pA AohA kpku  A sprl Aopunz ulhA.
Ol Dvuklylk pm ol zovBsk kpzjsvzl Aol AyBAo Av opz myplukz. PA DvBsk il h ypzrF tvCl. flz, Aol AyBAo DvBsk thrl Aopunz h svA lhzply pm AolF hss zAhFlk vu Aol zhtl whnl, iBA Aol AyBAo tpnoA myhjAByl Aol nyvBw slhCpun lClyFAopun pu lClu tvyl vm h tlzz Aohu pA Dhz uvA Alsspun Aol AyBAo. PA Dhz Aptl Av kljpkl Dopjo DhF Av nv.
aol klzlyA Dpuk islD Aol ABtislDllk pu myvuA vm Aol jhy. HslE zDlyClk Av hCvpk Aol ABtislDllk, iBA ol AByulk Aol Dolls h ipA Avv zAyvun huk Aol jhy slmA Aol yvhk huk zrpkklk vuAv Aol kpyA tlkphu. Ol puzAhuAsF zshttlk vu Aol iyhrlz huk Aol jhy zAvwwlk pu h jsvBk vm kpyA. dolu Aol kBzA jsvBk ohk zlAAslk huk ol jvBsk zll hyvBuk opt hnhpu, ol ylhspGlk AohA ol  k zvtlovD jyvzzlk vCly puAv hu luApylsF ulD kptluzpvu.
Ol olhyk Aol zvun jvtpun myvt h kpzAhujl, spnoAsF msvhApun vCly Aol hpy Av opz lhyz. HsAovBno pA Dhz zvmA huk jhstpun, ol Dhz DhyF. PA zlltlk h spAAsl Avv zvmA huk h spAAsl Avv jhstpun mvy lClyFAopun AohA Dhz nvpun vu. Ol DhuAlk pA Av il uvAopun tvyl Aohu ilhBApmBs tBzpj jvtpun myvt Aol puuvjluA huk wByl qvF vm zpunpun, iBA pu Aol ihjr vm opz tpuk, ol rulD pA Dhz sprlsF zvtl AFwl vm Ayhw.
aol hshyt DluA vmm huk Qhrl yvzl hDhrl. Ypzpun lhysF ohk iljvtl h khpsF ypABhs, vul AohA ol jvBsk uvA mBssF lEwshpu. Myvt Aol vBAzpkl, pA Dhz h Dvukly AohA ol Dhz hisl Av nlA Bw zv lhysF lhjo tvyupun mvy zvtlvul Dov ohk hizvsBAlsF uv wshuz Av il wyvkBjApCl kBypun Aol luApyl khF.
Wpur wvuplz huk wBywsl npyhmmlz yvhtlk Aol mplsk. JvAAvu jhukF nylD myvt Aol nyvBuk hz h jovjvshAl ypCly tlhuklylk vmm Av Aol zpkl. dohA svvrlk sprl zAvulz pu Aol whzAByl Dlyl hjABhssF yvjr jhukF. LClyFAopun pu oly kylht zlltlk Av il wlymljA lEjlwA mvy Aol mhjA AohA zol ohk uv tvBAo.
 PA kvlzu  A Ahrl tBjo Av AvBjo zvtlvul  z olhyA,  KhpzF zhpk DpAo h ztpsl vu oly mhjl.  PA  z vmAlu qBzA Aol spAAsl Aopunz FvB kv AohA jhu johunl h wlyzvu  z khF mvy Aol ilAAly.  KhpzF AyBsF ilsplClk Aopz Av il Aol DhF Aol Dvysk Dvyrlk, iBA zol kpku  A BuklyzAhuk AohA zol Dhz tlylsF h yvivA AohA ohk illu wyvnyhttlk Av ilsplCl Aopz.
aopunz hylu  A nvpun Dlss hA hss DpAo tvt AvkhF. Zol pz qBzA h sptw uvvksl huk DhuAz Av zsllw hss Aol Aptl. P zByl ovwl AohA Aopunz nlA ilAAly zvvu.
Zol svvrlk hA oly zABkluA Dvuklypun pm zol jvBsk lCly nlA AoyvBno.  fvB ullk Av slhyu Av Aopur mvy FvByzlsm,  zol DhuAlk Av Alss opt.  fvBy myplukz hyl ovskpun FvB ihjr huk iypunpun FvB kvDu.  IBA zol kpku  A iljhBzl zol rulD opz myplukz Dlyl hss AohA ol ohk huk lClu pm AohA tlhuA h spml vm tpzlyF, ol DvBsk ulCly npCl Aolt Bw.
PA hss zAhyAlk DpAo h yhukvt slAAly. ZlClyhs vm Aovzl Dlyl qvpulk mvyjlz Av jylhAl h yhukvt Dvyk. aol Dvykz kljpklk Av nlA AvnlAoly huk mvyt h yhukvt zluAlujl. aolF kljpklk uvA Av zAvw Aolyl huk pA Dhzu  A svun ilmvyl h yhukvt whyhnyhwo ohk illu jviislk AvnlAoly. aol xBlzApvu Dhz DolAoly vy uvA AolF jvBsk jvuApuBl Aol tvtluABt svun luvBno Av jylhAl h yhukvt zovyA zAvyF.
Ol jvBsku  A tvCl. Opz olhk Aoyviilk huk zwBu. Ol jvBsku  A kljpkl pm pA Dhz Aol msB vy Aol kypurpun shzA upnoA. PA Dhz wyvihisF h jvtipuhApvu vm ivAo.
Ol opk Bukly Aol jvClyz ovwpun AohA uvivkF DvBsk uvApjl opt Aolyl. PA ylhssF kpku  A thrl tBjo zluzl zpujl pA DvBsk il viCpvBz Av huFvul Dov Dhsrlk puAv Aol yvvt Aolyl Dhz zvtlvul opkpun Aolyl, iBA ol zApss olsk vBA ovwl. Ol olhyk mvvAzAlwz jvtpun kvDu Aol ohss huk zAvw pu myvuA pu myvuA vm Aol ilkyvvt kvvy. Ol olhyk Aol zxBlhr vm Aol kvvy opunlz huk zvtlvul vwlulk Aol ilkyvvt kvvy. Ol olsk opz iylhAo DhpApun mvy DovlCly Dhz hivBA Av kpzjvCly opt, iBA AolF ulCly kpk.
aol ispurpun spnoA jhBnoA oly hAAluApvu. Zol AovBnoA hivBA pA h ipA huk jvBsku  A yltltily lCly uvApjpun pA ilmvyl. aohA Dhz zAyhunl zpujl pA Dhz viCpvBz Aol mshzopun spnoA ohk illu Aolyl mvy Flhyz. UvD zol Dvuklylk ovD zol tpzzlk pA mvy AohA htvBuA vm Aptl huk DohA vAoly Aopunz pu oly zthss AvDu zol ohk mhpslk Av uvApjl.
PA Dhzu  A zBwwvzlk Av luk AohA DhF. aol wshu ohk illu tlApjBsvBzsF AovBnoA vBA huk wyhjApjlk hnhpu huk hnhpu. aolyl Dhz vusF vul wvzzpisl ylzBsA vujl pA ohk illu ptwsltluAlk, iBA hz AolF zAvvk Aolyl Aol ylzBsA Dhzu  A huFAopun jsvzl Av DohA pA zovBsk ohCl illu. aolF hss ishursF svvrlk hA lhjo Dvuklypun ovD Aopz jvBsk ohCl ohwwlulk. Pu Aolpy tpukz, AolF hss ilnhu Av ishtl Aol vAoly tltilyz vm Aol nyvBw hz Av DoF AolF ohk mhpslk.
Zol ohk illu Avsk Aptl huk Aptl hnhpu AohA Aol tvzA ptwvyAhuA zAlwz Dlyl Aol mpyzA huk Aol shzA. PA Dhz zvtlAopun AohA zol jhyyplk DpAopu oly pu lClyFAopun zol kpk, iBA Aolu ol zovDlk Bw huk kpzyBwAlk lClyFAopun. Ol Avsk oly AohA zol ohk pA Dyvun. aol mpyzA zAlw Dhzu  A Aol tvzA ptwvyAhuA. aol shzA zAlw Dhzu  A Aol tvzA ptwvyAhuA. PA Dhz Aol ulEA zAlw AohA Dhz Aol tvzA ptwvyAhuA.
ThuF wlvwsl zhF AohA spml pzu  A sprl h ilk vm yvzlz. P iln Av kpmmly. P Aopur AohA spml pz xBpAl sprl h ilk vm yvzlz. QBzA sprl spml, h ilk vm yvzlz svvrz wylAAF vu Aol vBAzpkl, iBA Dolu FvB  yl pu pA, FvB mpuk AohA pA pz uvAopun iBA Aovyuz huk whpu. P tFzlsm ohCl illu wypjrlk xBpAl ihksF.
aolyl Dhz spAAsl kvBiA AohA Aol iypknl Dhz Buzhml. Hss vul ohk Av kv Dhz svvr hA pA Av ruvD AohA DpAo jlyAhpuAF. flA Ivi kpku  A zll huvAoly vwApvu. Ol thF ohCl illu hisl Av Dvyr vul vBA pm ol ohk h ipA vm Aptl Av Aopur Aopunz AoyvBno, iBA Aptl Dhz zvtlAopun ol kpku  A ohCl. H jovpjl ullklk Av il thkl, huk pA ullklk Av il thkl xBpjrsF.
Kliipl wBA oly ohuk puAv Aol ovsl, zspkpun oly ohuk kvDu hz mhy hz oly hyt jvBsk ylhjo. Zol Dpnnslk oly mpunlyz ovwpun Av AvBjo zvtlAopun, iBA hss zol mlsA Dhz hpy. Zol zopmAlk Aol DlpnoA vm oly ivkF Av AyF huk ylhjo hu pujo vy ADv tvyl kvDu Aol ovsl. Oly mpunlyz zApss AvBjolk uvAopun iBA hpy.
Zsllwpun pu opz jhy Dhz ulCly Aol wshu iBA zvtlAptlz Aopunz kvu  A Dvyr vBA hz wshuulk. aopz ohk illu opz spml mvy Aol shzA Aoyll tvuAoz huk ol Dhz qBzA ilnpuupun Av nlA Bzlk Av pA. Ol kpku  A hjABhssF luqvF pA, iBA ol ohk hjjlwAlk pA huk jvtl Av Alytz DpAo pA. Vy hA slhzA ol AovBnoA ol ohk. Hss AohA johunlk Dolu ol wBA Aol rlF puAv Aol pnupApvu, AByulk pA huk Aol lunpul kpku  A thrl h zvBuk.
aDluAF-mpCl ovByz ohk whzzlk zpujl Aol pujpkluA. PA zlltlk Av il h svA svunly Aohu AohA. aohA ADluAF-mpCl ovByz zlltlk tvyl sprl h Dllr pu oly tpuk. aol mhjA AohA zol zApss Dhz ohCpun AyvBisl jvtwylolukpun lEhjAsF DohA Avvr wshjl Dhzu  A olswpun Aol thAAly. Zol AovBnoA pm zol jvBsk qBzA nlA h spAAsl ylzA Aol luApyl pujpkluA tpnoA thrl h spAAsl tvyl zluzl.
LhApun yhD mpzo kpku  A zvBuk sprl h nvvk pklh.  PA  z h klspjhjF pu Qhwhu,  kpku  A zllt Av thrl pA huF tvyl hwwlApGpun. YhD mpzo pz yhD mpzo, klspjhjF vy uvA.
Zol nshujlk Bw puAv Aol zrF Av DhAjo Aol jsvBkz Ahrpun zohwl. MpyzA, zol zhD h kvn. UlEA, pA Dhz hu lslwohuA. MpuhssF, zol zhD h nphuA Btiylssh huk hA AohA tvtluA Aol yhpu ilnhu Av wvBy.
Ol Dhz hmAly Aol AyBAo. HA slhzA, AohA  z DohA ol Avsk optzlsm. Ol ilsplClk pA, iBA huF yhApvuhs wlyzvu vu Aol vBAzpkl jvBsk zll ol Dhz sFpun Av optzlsm. PA Dhz hwwhyluA ol Dhz ylhssF vusF hmAly opz vDu AyBAo AohA ol  k hsylhkF kljpklk huk Dhz hmAly Aopz AyBAo iljhBzl Aol mhjAz kpku  A spul Bw DpAo Aol AyBAo ol DhuAlk. Zv ol jvuApuBlk Av Alss lClyFvul ol Dhz hmAly Aol AyBAo vispCpvBz Av Aol ylhs AyBAo zpAApun ypnoA pu myvuA vm opt.
Hjjvykpun Av Aol jhwApvu vu Aol iyvuGl thyrly wshjlk iF Aol TBsAuvtho JohwAly vm Aol KhBnoAlyz vm Aol Htlypjhu YlCvsBApvu vu ThF 12, 1939, Jvsslnl Ohss (pz) Aol vsklzA iBpskpun pu jvuApuBvBz Bzl mvy LkBjhApvuhs wBywvzlz DlzA vm Aol YvjrF TvBuAhpuz. Olyl Dlyl lkBjhAlk tlu huk Dvtlu Dov ohCl Dvu yljvnupApvu AoyvBnovBA Aol Dvysk pu hss Aol slhyulk wyvmlzzpvuz.
 Zv, DohA kv FvB Aopur?  ol hzrlk ulyCvBzsF. Ol DhuAlk Av ruvD Aol huzDly, iBA hA Aol zhtl Aptl, ol kpku  A. Ol  k wBA opz olhyA huk zvBs puAv Aol wyvqljA huk ol Dhzu  A zByl ol  k il hisl Av yljvCly pm AolF kpku  A sprl DohA ol wyvkBjlk. aol zpslujl myvt Aol vAolyz pu Aol yvvt zlltlk Av shzA h spmlAptl lClu AovBno pA ohk vusF illu h tvtluA zpujl ol hzrlk Aol xBlzApvu.  Zv, DohA kv FvB Aopur?  ol hzrlk hnhpu.
Zol zhA kvDu DpAo oly uvAlivvr pu oly ohuk, oly tpuk Dhuklypun Av mhyhDhF wshjlz. Zol whBzlk huk jvuzpklylk hss AohA ohk ohwwlulk. PA ohku  A nvul hz lEwljAlk. dolu Aol khF ilnhu zol AovBnoA pA Dhz nvpun Av il h ihk vul, iBA hz zol zhA yljhsspun Aol khF  z lCluAz Av DypAl Aolt kvDu, zol ohk Av hktpA, pA ohk illu h yhAoly thyClsvBz khF.
Zol  z hzrlk Aol xBlzApvu zv thuF Aptlz AohA zol ihylsF spzAlulk Av Aol huzDlyz huFtvyl. aol huzDlyz Dlyl hsDhFz Aol zhtl. dlss, uvA lEhjAsF Aol zhtl, iBA Aol zhtl pu h nlulyhs zluzl. H tvyl hjjByhAl klzjypwApvu Dhz Aol huzDlyz ulCly zBywypzlk oly. Zv, zol hzrlk mvy Aol 10,000Ao Aptl,  dohA  z FvBy mhCvypAl hupths?  IBA Aopz Aptl Dhz kpmmlyluA. dolu zol olhyk Aol FvBun ivF  z huzDly, zol Dvuklylk pm zol ohk olhyk opt jvyyljAsF.
Ol Avvr h zpw vm Aol kypur. Ol Dhzu  A zByl DolAoly ol sprlk pA vy uvA, iBA hA Aopz tvtluA pA kpku  A thAAly. Zol ohk thkl pA lzwljphssF mvy opt zv ol DvBsk ohCl mvyjlk pA kvDu lClu pm ol ohk hizvsBAlsF ohAlk pA. aohA  z zptwsF Aol DhF Aopunz Dvyrlk. Zol thkl opt h ulD-mhunslk kypur lhjo khF huk ol Avvr h zpw vm pA huk ztpslk, zhFpun pA Dhz lEjlssluA.
Hz zol zhA DhAjopun Aol Dvysk nv iF, zvtlAopun jhBnoA oly lFl. PA Dhzu  A zv tBjo pAz jvsvy vy zohwl, iBA Aol DhF pA Dhz tvCpun. Zol zxBpuAlk Av zll pm zol jvBsk ilAAly BuklyzAhuk DohA pA Dhz huk Dolyl pA Dhz nvpun, iBA pA kpku  A olsw. Hz zol jvuApuBlk Av zAhyl puAv Aol kpzAhujl, zol kpku  A BuklyzAhuk DoF Aopz Bulhzpulzz Dhz iBpskpun puzpkl oly ivkF. Zol mlsA sprl zol zovBsk nlA Bw huk yBu. Pm vusF zol jvBsk thrl vBA DohA pA Dhz. HA AohA tvtluA, zol jvtwyloluklk DohA pA Dhz huk Dolyl pA Dhz olhkpun, huk zol rulD oly spml DvBsk ulCly il Aol zhtl.
aol whwly Dhz ishur. PA zovBsku  A ohCl illu. aolyl zovBsk ohCl illu DypApun vu Aol whwly, hA slhzA h whyhnyhwo pm uvA tvyl. aol mhjA AohA Aol DypApun Dhzu  A Aolyl Dhz myBzAyhApun. HjABhssF, pA Dhz lClu tvyl Aohu myBzAyhApun. PA Dhz kvDuypnoA kpzAylzzpun.
aolF yBzolk vBA Aol kvvy, nyhiipun huFAopun huk lClyFAopun AolF jvBsk Aopur vm AolF tpnoA ullk. aolyl Dhz uv Aptl Av kvBisl-joljr Av thrl zByl AolF Dlylu  A slhCpun zvtlAopun ptwvyAhuA ilopuk. LClyFAopun Dhz AoyvDu puAv Aol jhy huk AolF zwlk vmm. aopyAF tpuBAlz shAly AolF Dlyl zhml huk AohA Dhz Dolu pA khDulk vu Aolt AohA AolF ohk mvynvAAlu Aol tvzA ptwvyAhuA Aopun vm hss.
aolyl Dlyl ADv Aopunz AohA Dlyl ptwvyAhuA Av ayhjlF. aol mpyzA Dhz oly kvn. HuFvul AohA ohk lCly tlA ayhjlF rulD ovD tBjo zol svClk oly kvn. TvzA DvBsk zhF AohA zol AylhAlk pA hz oly jopsk. aol kvn DluA lClyFDolyl DpAo oly huk pA ohk illu oly ilzA mypluk mvy Aol whzA mpCl Flhyz. aol zljvuk Aopun AohA Dhz ptwvyAhuA Av ayhjlF, ovDlCly, DvBsk il h svA tvyl zBywypzpun Av tvzA wlvwsl.
aol ylk spul tvClk hjyvzz Aol whnl. dpAo lhjo tpssptlAly pA hkChujlk mvyDhyk, zvtlAopun johunlk pu Aol yvvt. aol hjABhs johunl Ahrpun wshjl Dhz kpmmpjBsA Av wlyjlpCl, iBA Aol johunl Dhz ylhs. aol ylk spul jvuApuBlk ylsluAslzzsF hjyvzz Aol whnl huk Aol yvvt DvBsk ulCly il Aol zhtl.
Zol wBA Aol wlu Av whwly iBA zol jvBsku  A iypun olyzlsm Av hjABhssF DypAl huFAopun. Zol qBzA zAhylk hA Aol ishur jhyk huk Dvuklylk DohA Dvykz zol jvBsk DypAl AohA DvBsk olsw pu lClu h zthss DhF. Zol AovBnoA vm h kvGlu DhFz Av ilnpu iBA uvul zlltlk Av kv qBzApjl Av Aol zpABhApvu. aolyl Dlyl uv Dvykz AohA jvBsk olsw huk zol rulD pA.
av Aol ADv myplukz, Aol AyllovBzl Dhz tBjo tvyl Aohu h AyllovBzl. PA Dhz h zhujABhyF hDhF myvt Aol vAoly rpkz Dolyl AolF jvBsk il AoltzlsClz DpAovBA ilpun Alhzlk vy iBssplk. PA Dhz Aolpy zljylA mvyAylzz opkklu opno pu Aol iyhujolz vm h oBnl vhr AohA vusF AolF rulD lEpzAlk. HA slhzA AohA pz DohA AolF AovBnoA. aolF Dlyl tvyl Aohu h spAAsl huuvFlk Dolu Aolpy ADv FvBunly zpzAlyz kljpklk Av AByu Aol AyllovBzl puAv h wypujlzz jhzAsl iF whpuApun Aol puzpkl wpur huk wBAApun nspAAly lClyFDolyl.
aol htily kyvwslA oBun myvt Aol iyhujo, ylhjopun mBssulzz huk ylhkF Av kyvw. PA DhpAlk. dopsl thuF vm Aol vAoly kyvwslAz Dlyl zhApzmplk Av mvyt hz ipn hz AolF jvBsk huk ylslhzl, Aopz kyvwslA ohk vAoly wshuz. PA DhuAlk Av il whyA vm opzAvyF. PA DhuAlk Av il yltltilylk svun hmAly hss Aol vAoly kyvwslAz ohk kpzzvsClk puAv opzAvyF. Zv pA DhpAlk mvy Aol wlymljA zwljptlu Av msF iF Av Ayhw huk jhwAByl AohA pA ovwlk DvBsk lCluABhssF il kpzjvClylk oBukylkz vm Flhyz pu Aol mBAByl.
aol iypknl zwhuupun h 100-mvvA nBssF zAvvk pu myvuA vm opt hz Aol shzA vizAhjsl isvjrpun opt myvt ylhjopun opz klzApuhApvu. dopsl wlvwsl thF ohCl jhsslk pA h  iypknl , Aol ylhspAF Dhz pA Dhz uvAopun tvyl Aohu zwspuAlylk Dvvklu wshurz olsk AvnlAoly iF yvAApun yvwlz. PA Dhz xBlzApvuhisl DolAoly pA DvBsk ovsk Aol DlpnoA vm h jopsk, slA hsvul Aol DlpnoA vm h nyvDu thu. aol wyvislt Dhz Aolyl Dhz uv vAoly DhF hjyvzz Aol nBssF, huk Aopz wshFlk puAv opz jhsjBshApvuz vm DolAoly vy uvA pA Dhz DvyAo Aol ypzr vm AyFpun Av jyvzz pA.
PA wyvihisF zlltlk AypCphs Av tvzA wlvwsl, iBA pA thAAlylk Av ayhjlF. Zol Dhzu  A zByl DoF pA thAAlylk zv tBjo Av oly, iBA zol BuklyzAvvk kllw DpAopu oly ilpun AohA pA thAAlylk Av oly. Zv mvy Aol 365Ao khF pu h yvD, ayhjlF zhA kvDu Av lhA whujhrlz mvy iylhrmhzA.
Ol Dhsrlk kvDu Aol zAlwz myvt Aol Ayhpu zAhApvu pu h ipA vm h oByyF ruvDpun Aol zljylAz pu Aol iyplmjhzl tBzA il zljBylk hz xBpjrsF hz wvzzpisl. IvBukpun kvDu Aol zAlwz, ol olhyk zvtlAopun ilopuk opt huk xBpjrsF AByulk pu h whupj. aolyl Dhz uvivkF Aolyl iBA h whpy vm vsk Dvyu-vBA zovlz Dlyl wshjlk ulhAsF vu Aol zAlwz ol ohk qBzA jvtl kvDu. Ohk ol whzA Aolt DpAovBA zllpun Aolt? PA kpku  A zllt wvzzpisl. Ol Dhz hivBA Av AByu huk il vu opz DhF Dolu h kllw jopss mpsslk opz ivkF.
Ovwlz huk kylhtz Dlyl khzolk AohA khF. PA zovBsk ohCl illu lEwljAlk, iBA pA zApss jhtl hz h zovjr. aol Dhyupun zpnuz ohk illu pnuvylk pu mhCvy vm Aol wvzzpipspAF, ovDlCly yltvAl, AohA pA jvBsk hjABhssF ohwwlu. aohA wvzzpipspAF ohk nyvDu myvt ovwl Av hu Bukluphisl ilsplm pA tBzA il klzApuF. aohA Dhz BuAps pA Dhzu  A huk Aol ovwlz huk kylhtz jhtl jyhzopun kvDu.
aDluAF-mpCl Flhyz Khuh ohk illu DhpApun. Zol Ayplk Av il whApluA kBypun AohA Aptl iBA zol ohku  A hsDhFz thuhnlk Av il hz whApluA hz zol  k sprl. IBA AvkhF Aol vwwvyABupAF ohk mpuhssF jvtl. aol Aopun zol hsDhFz pthnpulk DvBsk thrl oly Aol ohwwplzA wlyzvu pu Aol Dvysk Dhz hivBA Av ohwwlu. Zol kpku  A ruvD DoF hA Aopz zwljpmpj Aptl zol hss vm h zBkklu mlsA zpjr puzpkl.
SvCl pzu  A hsDhFz h yhF vm zBuzopul. aohA  z DohA Aol vskly npysz rlwA Alsspun oly Dolu zol zhpk zol ohk mvBuk Aol wlymljA thu. Zol ohk AovBnoA Aopz Dhz zptwsF ipAAly Ahsr vu Aolpy whyA zpujl AolF ohk illu Buhisl Av mpuk AyBl svCl sprl olyz. IBA uvD zol ohk Av mhjl Aol mhjA AohA AolF thF ohCl illu ypnoA. SvCl thF uvA hsDhFz il h yhF vm zBuzopul. aohA pz Buslzz AolF Dlyl ylmlyypun Av ovD Aol zBu jhu iByu.
Kliipl rulD zol Dhz ilpun zlsmpzo huk Buylhzvuhisl. Zol BuklyzAvvk DoF Aol vAolyz pu Aol yvvt Dlyl hunyF huk myBzAyhAlk DpAo oly huk Aol DhF zol Dhz hjApun. Pu oly lFlz, pA kpku  A ylhssF thAAly ovD AolF mlsA iljhBzl zol zptwsF kpku  A jhyl.
Kv FvB Aopur FvB  yl spCpun hu vykpuhyF spml? fvB hyl zv tpzAhrlu pA  z kpmmpjBsA Av lClu lEwshpu. aol tlyl mhjA AohA FvB lEpzA thrlz FvB lEAyhvykpuhyF. aol vkkz vm FvB lEpzApun hyl slzz Aohu Dpuupun Aol svAAlyF, iBA olyl FvB hyl. Hyl FvB nvpun Av slA Aopz lEAyhvykpuhyF vwwvyABupAF whzz?
aolyl Dlyl spAAsl Aopunz AohA zol zptwsF jvBsk uvA zAhuk. aol zvBuk vm zvtlvul Ahwwpun Aolpy uhpsz vu Aol Ahisl. H wlyzvu jolDpun DpAo Aolpy tvBAo vwlu. HuvAoly oBthu ptwvzpun AoltzlsClz puAv oly zwhjl. Zol jvBsku  A zAhuk huF vm Aolzl Aopunz, iBA uvul vm Aolt jvtwhylk Av Aol uBtily vul Aopun zol jvBsku  A zAhuk Dopjo Avwwlk hss vm Aolt jvtipulk. """

assert test_cipher.auto_decrypt_bonus(long_ciphertext, english_word_list, verbose=False) == (long_plaintext, 'h')