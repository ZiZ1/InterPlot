def generate_metadata(title,author,description=None,enable_warning=False):
    """
    The function generates metadata for saving a file in png format. 
    It pastes current working directory as a source of data, writes 
    data and time of plot generation, 
    
    Parameters:
    ----------
    title : str
            Short (one line) title or caption for image
    author: str
            Author
    description: str
            Description of image (possibly long)
    comments : str
             Any miscellaneous comments
    
    Dependencies
    ------------
    os
    daytime
    
    Returns:
    -------
    metadata  : dict
    """
    metadata = {'Title':  title,
                'Author': author
                }
    if description is not None:
        metadata['Description'] = description
    if enable_warning:
        metadata['Warning'] = 'Caution: science!'

    # Getting time
    now = datetime.datetime.now()
    string_time = now.strftime("%Y-%m-%d %H:%M")
    metadata['Creation Time'] = string_time
    
    metadata['Comment']= "Path to the source: {}".format(os.getcwd())
    return metadata
