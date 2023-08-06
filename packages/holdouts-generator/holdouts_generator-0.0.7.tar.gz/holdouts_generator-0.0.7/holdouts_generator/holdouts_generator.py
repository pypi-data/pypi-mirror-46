import os
import pickle
import shutil
from auto_tqdm import tqdm
from typing import List, Tuple


def load_cache(dataset, holdout, name, cache_dir:str):
    """Return given holdout, also handles cache if it is enabled."""
    path = "{cache_dir}/{name}.pickle".format(cache_dir=cache_dir, name=name)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    os.makedirs(cache_dir, exist_ok=True)
    data = holdout(dataset)
    with open(path, "wb") as f:
        pickle.dump(data, f)
    return data

def get_desc(level:int):
    if level==0:
        return "Holdouts"
    if level==1:
        return "Inner holdouts"
    if level>1:
        return "Inner holdouts (level {level})".format(level=level)


def holdouts_generator(*dataset, holdouts:List, verbose:bool=True, cache:bool=False, cache_dir:str=".holdouts", level:int=0):
    """Return validation dataset and another holdout generator
        dataset, iterable of datasets to generate holdouts from.
        holdouts:List, list of holdouts callbacks.
        verbose:bool=True, whetever to show or not loading bars.
        cache:bool=False, whetever to cache or not the rendered holdouts.
        cache_dir:str=".cache", directory where to cache the holdouts.
    """
    def generator():
        for outer_holdout, name, inner_holdouts in tqdm(list(holdouts), verbose=verbose, desc=get_desc(level)):
            validation = load_cache(dataset, outer_holdout, name, cache_dir) if cache else outer_holdout(dataset)
            training, testing = validation[::2], validation[1::2]
            if inner_holdouts is None:
                yield (training, testing), None
            else:
                yield (training, testing), holdouts_generator(
                    *training,
                    holdouts=inner_holdouts,
                    verbose=verbose,
                    cache=cache,
                    cache_dir="{cache_dir}/{name}".format(
                        cache_dir=cache_dir,
                        name=name
                    ),
                    level=level+1
                )
    return generator


def clear_holdouts_cache(cache_dir:str=".holdouts"):
    """Remove the holdouts cace directory.
        cache_dir:str=".holdouts", the holdouts cache directory to be removed.
    """
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)