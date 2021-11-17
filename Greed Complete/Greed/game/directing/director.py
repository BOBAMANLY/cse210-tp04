class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service, score):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self.score = score
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        # get direction to move from keyboard service
        player = cast.get_first_actor("player")
        velocity = self._keyboard_service.get_direction()
        player.set_velocity(velocity)        
        # player actor = direction horizontal only
    

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        # create rocks, gems at top of screen (random x, set y)(random number of stones)
        cast.add_actor("stone", "O")
        cast.add_actor("gem", "*")
        # move player, rocks, gems
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        for actor in cast.get_all_actors():
            actor.move_next(max_x, max_y)
        # check for collisions between player and stone or player and gem
        # award points if needed(add points to score, negative for rocks, positive for gems)
        # remove stone or gem if needed
        if cast.get_first_actor("player").get_position() == cast.get_first_actor("stone").get_position():
            self.score.add_points(-1)
            cast.remove_actor("stone", "O")
        elif cast.get_first_actor("player").get_position() == cast.get_first_actor("gem").get_position():
            self.score.add_points(1)
            cast.remove_actor("gem", "*")
        

        
        
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()