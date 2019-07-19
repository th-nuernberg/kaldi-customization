export * from './project.service';
import { ProjectService } from './project.service';
export * from './user.service';
import { UserService } from './user.service';
export const APIS = [ProjectService, UserService];
