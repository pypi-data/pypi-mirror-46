# Treep, copyright 2019 Max Planck Gesellschaft
# Author : Vincent Berenz 

# This file is part of Treep.

#    Treep is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Treep is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Treep.  If not, see <https://www.gnu.org/licenses/>.


import copy

class Project(object):

    __slots__ = ["name","parent_projects",
                 "repositories","users",
                 "parents"]
    
    def  __init__(self,
                  name,
                  parent_projects,
                  repositories,
                  users=None):
        """ 
        Parameters
        ----------
        name: str
            name of this project
        projects: list of Projects 
            iterable of instance of projects that will be included in this project
        repositories : list of str
            list of names of repos contained by this project
        users: list of str, optional
            list of user names of this project
        """
        self.name = name
        self.parent_projects = parent_projects
        self.repositories = repositories
        self.users = None

    def get_users(self):
        return copy.deepcopy(self._users)

    
        
        
