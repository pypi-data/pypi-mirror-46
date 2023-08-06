class WordSearch:
  def __init__(self, search):
    self.search = search
    self.ssearch = []
    if self.search.find(' ') == -1:
      for x in range(len(self.search)):
        self.ssearch.append(self.search[x])

    if self.search.find(' ') != -1:
      self.ssearch = self.search.split(' ')
      for x in self.ssearch:
        if len(x) > 1:
          self.ssearch.insert(self.ssearch.index(x)+1,'\n')
          self.ssearch.insert(self.ssearch.index(x)+2,x[-1])
          self.ssearch[self.ssearch.index(x)] = x[0]

    self.length_o_row = self.ssearch.index('\n')

    self.rows = [i for i, x in enumerate(self.ssearch) if x == '\n']
    for x in self.rows:
      self.ssearch.remove("\n")

    self.dir_list = []

    self.final_list = []

    self.ssearch_copy = [i for i in self.ssearch]

  def Words(self, lwords = None):
    if isinstance(lwords, list):
      self.words = lwords
      self.swords = []
      for word in lwords:
        temp_list = []
        for x in range(len(word)):
          temp_list.append(word[x])
        self.swords.append(temp_list)
      self.fletters = []
      for word in lwords:
        temp2 = [i for i, x in enumerate(self.ssearch) if x == word[0]]
        self.fletters.append(temp2)
      return "Now 'Solve()' and you will have a list of solutions."
    else:
      print('Params need to be a list for "Word" function.')

  def Solve(self):
    for sword in self.swords:
      word_found = False
      wordf2 = True
      for lis in self.fletters:
        if word_found:
          break
        for x in lis:
          letter_matches_d = []
          temp_list = []
          for y in range(1,len(sword)):
            try:
              if x not in temp_list:
                temp_list.append(x)
              if self.ssearch[x+(self.length_o_row*y)] == sword[y]:
                temp_list.append(x+(self.length_o_row*y))
                if len(temp_list) == len(sword):
                  for i,l in enumerate(temp_list):
                    if self.ssearch[l] != sword[i]:
                      wordf2 = False
                  if wordf2:
                    letter_matches_d.append(temp_list)
                    self.final_list.append(letter_matches_d)
                    self.dir_list.append('Top - Bottom')
                    word_found = True
            except IndexError:
              pass

    for sword in self.swords:
      word_found = False
      wordf2 = True
      for lis in self.fletters:
        if word_found:
          break
        for x in lis:
          letter_matches_dr = []
          temp_list = []
          for y in range(1,len(sword)):
            try:
              if x not in temp_list:
                temp_list.append(x)
              if self.ssearch[x+(self.length_o_row*y)+(1*y)] == sword[y]:
                temp_list.append(x+(self.length_o_row*y)+(1*y))
                if len(temp_list) == len(sword):
                  for i,l in enumerate(temp_list):
                    if self.ssearch[l] != sword[i]:
                      wordf2 = False
                  if wordf2:
                    letter_matches_dr.append(temp_list)
                    self.final_list.append(letter_matches_dr)
                    self.dir_list.append('Top - Bottom right')
                    word_found = True
            except IndexError:
              pass

    for sword in self.swords:
      word_found = False
      wordf2 = True
      for lis in self.fletters:
        if word_found:
          break
        for x in lis:
          letter_matches_dl = []
          temp_list = []
          for y in range(1,len(sword)):
            try:
              if x not in temp_list:
                temp_list.append(x)
              if self.ssearch[x+(self.length_o_row*y)-(1*y)] == sword[y]:
                temp_list.append(x+(self.length_o_row*y)-(1*y))
                if len(temp_list) == len(sword):
                  for i,l in enumerate(temp_list):
                    if self.ssearch[l] != sword[i]:
                      wordf2 = False
                  if wordf2:
                    letter_matches_dl.append(temp_list)
                    self.final_list.append(letter_matches_dl)
                    self.dir_list.append('Top - Bottom left')
                    word_found = True
            except IndexError:
              pass

    for sword in self.swords:
      word_found = False
      wordf2 = True
      for lis in self.fletters:
        if word_found:
          break
        for x in lis:
          letter_matches_u = []
          temp_list = []
          for y in range(1,len(sword)):
            try:
              if x not in temp_list:
                temp_list.append(x)
              if self.ssearch[x-(self.length_o_row*y)] == sword[y]:
                temp_list.append(x-(self.length_o_row*y))
                if len(temp_list) == len(sword):
                  for i,l in enumerate(temp_list):
                    if self.ssearch[l] != sword[i]:
                      wordf2 = False
                  if wordf2:
                    letter_matches_u.append(temp_list)
                    self.final_list.append(letter_matches_u)
                    self.dir_list.append('Bottom - Top')
                    word_found = True
            except IndexError:
              pass

    for sword in self.swords:
      word_found = False
      wordf2 = True
      for lis in self.fletters:
        if word_found:
          break
        for x in lis:
          letter_matches_ur = []
          temp_list = []
          for y in range(1,len(sword)):
            try:
              if x not in temp_list:
                temp_list.append(x)
              if self.ssearch[x-(self.length_o_row*y)+(1*y)] == sword[y]:
                temp_list.append(x-(self.length_o_row*y)+(1*y))
                if len(temp_list) == len(sword):
                  for i,l in enumerate(temp_list):
                    if self.ssearch[l] != sword[i]:
                      wordf2 = False
                  if wordf2:
                    letter_matches_ur.append(temp_list)
                    self.final_list.append(letter_matches_ur)
                    self.dir_list.append('Bottom - Top right')
                    word_found = True
            except IndexError:
              pass

    for sword in self.swords:
      word_found = False
      wordf2 = True
      for lis in self.fletters:
        if word_found:
          break
        for x in lis:
          letter_matches_ul = []
          temp_list = []
          for y in range(1,len(sword)):
            try:
              if x not in temp_list:
                temp_list.append(x)
              if self.ssearch[x-(self.length_o_row*y)-(1*y)] == sword[y]:
                temp_list.append(x-(self.length_o_row*y)-(1*y))
                if len(temp_list) == len(sword):
                  for i,l in enumerate(temp_list):
                    if self.ssearch[l] != sword[i]:
                      wordf2 = False
                  if wordf2:
                    letter_matches_ul.append(temp_list)
                    self.final_list.append(letter_matches_ul)
                    self.dir_list.append('Bottom - Top left')
                    word_found = True
            except IndexError:
              pass

    for sword in self.swords:
      word_found = False
      wordf2 = True
      for lis in self.fletters:
        if word_found:
          break
        for x in lis:
          letter_matches_l = []
          temp_list = []
          for y in range(1,len(sword)):
            try:
              if x not in temp_list:
                temp_list.append(x)
              if self.ssearch[x-(1*y)] == sword[y]:
                temp_list.append(x-(1*y))
                if len(temp_list) == len(sword):
                  for i,l in enumerate(temp_list):
                    if self.ssearch[l] != sword[i]:
                      wordf2 = False
                  if wordf2:
                    letter_matches_l.append(temp_list)
                    self.final_list.append(letter_matches_l)
                    self.dir_list.append('Right - Left')
                    word_found = True
            except IndexError:
              pass

    for sword in self.swords:
      word_found = False
      wordf2 = True
      for lis in self.fletters:
        if word_found:
          break
        for x in lis:
          letter_matches_r = []
          temp_list = []
          for y in range(1,len(sword)):
            try:
              if x not in temp_list:
                temp_list.append(x)
              if self.ssearch[x+(1*y)] == sword[y]:
                temp_list.append(x+(1*y))
                if len(temp_list) == len(sword):
                  for i,l in enumerate(temp_list):
                    if self.ssearch[l] != sword[i]:
                      wordf2 = False
                  if wordf2:
                    letter_matches_r.append(temp_list)
                    self.final_list.append(letter_matches_r)
                    self.dir_list.append('Left - Right')
                    word_found = True
            except IndexError:
              pass

    done = []
    for i,list1 in enumerate(self.final_list):
      self.ssearch = [i for i in self.ssearch_copy]
      for list2 in list1:
        fword = ''
        final_search = ''
        output = ''''''
        for index in list2:
          fword += self.ssearch[index]
          self.ssearch[index] = '_'
        for row in self.rows:
          self.ssearch.insert(row, '\n')
        for letter in self.ssearch:
          final_search += ' '+letter
        output += final_search+'\n\n'+fword.title()+'\n\n'+self.dir_list[i]+'\n\n'
        done.append(output)

    return done