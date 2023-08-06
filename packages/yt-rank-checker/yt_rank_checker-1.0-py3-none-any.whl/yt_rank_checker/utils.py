def search_query(query):
        base = "https://www.youtube.com/results?search_query="
        split_list = query.split()
        #remove last element of list so addition signs can be added to first parts of the query
        last_element_removed = split_list[:-1]
        for word in last_element_removed:
          base = base + word + '+'

        #grab last element in list to append to end of query
        last_element_of_list = split_list[-1]
        final_query = base + last_element_of_list
        print(' ')
        print(final_query)
        print(' ')
        return final_query